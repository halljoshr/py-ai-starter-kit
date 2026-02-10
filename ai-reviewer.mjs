/* global process, console, Buffer, AbortController, setTimeout, clearTimeout, TextDecoder */
import {
    BedrockRuntimeClient,
    InvokeModelCommand,
} from "@aws-sdk/client-bedrock-runtime";
import { Octokit } from "@octokit/rest";
import { appendFileSync } from "fs";

// --- Configuration ---

const MODEL_ID = process.env.REVIEW_MODEL || "us.anthropic.claude-sonnet-4-5-20250929-v1:0";

/** Parse Bedrock model ID into a display name, e.g. "Claude Sonnet 4.5" */
function formatModelName(modelId) {
    const match = modelId.match(/claude-(\w+)-([\d-]+)/);
    if (!match) return modelId;
    const name = match[1].charAt(0).toUpperCase() + match[1].slice(1);
    const version = match[2].replace(/-/g, ".").replace(/\.v\d+$/, "").replace(/\.\d{8}$/, "");
    return `Claude ${name} ${version}`;
}

const MODEL_NAME = formatModelName(MODEL_ID);
const MAX_TOKENS = 4096;
const MAX_DIFF_BYTES = 100_000;
const MAX_INLINE_COMMENTS = 25;
const MAX_RETRIES = 3;
const BEDROCK_TIMEOUT_MS = 120_000;
const MAX_PR_BODY_LENGTH = 2000;
const REGION = "us-east-1";

const {
    GITHUB_TOKEN,
    PR_NUMBER,
    REPO_OWNER,
    REPO_NAME,
    PR_TITLE,
    PR_BODY,
    DRY_RUN,
    GITHUB_OUTPUT,
    GITHUB_SERVER_URL,
    GITHUB_REPOSITORY,
    GITHUB_RUN_ID,
} = process.env;

const prNumber = parseInt(PR_NUMBER, 10);
const isDryRun = DRY_RUN === "true";

// --- Clients ---

const bedrock = new BedrockRuntimeClient({ region: REGION });
const octokit = new Octokit({ auth: GITHUB_TOKEN });

// --- File priority for sorting ---

const FILE_PRIORITY = [
    { pattern: /^app\/routes\//, weight: 1 },
    { pattern: /^app\/lib\//, weight: 2 },
    { pattern: /^app\/components\//, weight: 3 },
    { pattern: /^packages\//, weight: 4 },
    { pattern: /^prisma\//, weight: 5 },
    { pattern: /^app\//, weight: 6 },
    { pattern: /\.(ts|tsx|js|jsx|mjs)$/, weight: 7 },
    { pattern: /\./, weight: 10 },
];

function getFilePriority(filename) {
    for (const { pattern, weight } of FILE_PRIORITY) {
        if (pattern.test(filename)) return weight;
    }
    return 10;
}

// --- Diff position mapping ---

/**
 * Parse a file's patch string to build a map from source line number
 * to GitHub diff position (1-indexed offset within the patch).
 *
 * GitHub review comments require a `position` that is the 1-based line
 * offset within the unified diff hunk, counting every line including
 * hunk headers, context lines, additions, and deletions.
 */
function buildLineToPositionMap(patch) {
    if (!patch) return new Map();

    const lines = patch.split("\n");
    const map = new Map();
    let position = 0;
    let currentLine = 0;

    for (const line of lines) {
        // Hunk header: @@ -oldStart,oldCount +newStart,newCount @@
        const hunkMatch = line.match(/^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
        if (hunkMatch) {
            position++;
            currentLine = parseInt(hunkMatch[1], 10);
            continue;
        }

        if (position === 0) continue; // Before first hunk

        position++;

        if (line.startsWith("+")) {
            // Added line — maps to the new file's line number
            map.set(currentLine, position);
            currentLine++;
        } else if (line.startsWith("-")) {
            // Removed line — no new-file line number, skip
        } else {
            // Context line
            map.set(currentLine, position);
            currentLine++;
        }
    }

    return map;
}

// --- Fetch PR files ---

async function fetchPRFiles() {
    const files = [];
    let page = 1;

    while (page <= 10) {
        const { data } = await octokit.pulls.listFiles({
            owner: REPO_OWNER,
            repo: REPO_NAME,
            pull_number: prNumber,
            per_page: 100,
            page,
        });

        files.push(...data);
        if (data.length < 100) break;
        page++;
    }

    return files;
}

// --- Prioritize and truncate diff ---

function prepareDiffContent(files) {
    // Sort by priority (routes/lib first, config/docs last)
    const sorted = [...files].sort(
        (a, b) => getFilePriority(a.filename) - getFilePriority(b.filename)
    );

    let totalBytes = 0;
    let truncated = false;
    const included = [];

    for (const file of sorted) {
        const patch = file.patch || "";
        const patchBytes = Buffer.byteLength(patch, "utf8");

        if (totalBytes + patchBytes > MAX_DIFF_BYTES) {
            truncated = true;
            // Include partial if we have room — truncate at last complete line
            // to avoid splitting multi-byte UTF-8 characters or diff hunks
            const remaining = MAX_DIFF_BYTES - totalBytes;
            if (remaining > 500) {
                const cutoff = patch.lastIndexOf("\n", remaining);
                if (cutoff > 0) {
                    included.push({
                        ...file,
                        patch: patch.slice(0, cutoff) + "\n... [truncated]",
                    });
                }
            }
            break;
        }

        included.push(file);
        totalBytes += patchBytes;
    }

    return { files: included, truncated, totalFiles: files.length };
}

// --- Build the review prompt ---

function buildPrompt(prFiles, truncated, totalFiles) {
    const truncationNotice = truncated
        ? `\n**Note:** The diff was truncated to fit within context limits. ${prFiles.length} of ${totalFiles} files are shown, prioritized by importance (routes > lib > components > config).`
        : "";

    const diffContent = prFiles
        .map(
            (f) =>
                `### ${f.filename} (${f.status}, +${f.additions}/-${f.deletions})\n\`\`\`diff\n${f.patch || "(binary or empty)"}\n\`\`\``
        )
        .join("\n\n");

    const systemPrompt = `You are a senior code reviewer. Your job is to find REAL bugs — code that WILL crash, produce wrong data, or leak secrets at runtime. You must NEVER report speculative, theoretical, or style-based issues.

CRITICAL: Only report CONFIRMED bugs, not POTENTIAL bugs. Every issue you report must be something that WILL fail, not something that MIGHT fail. If you cannot prove it breaks with a specific input, it is not a bug — do NOT report it. Reporting a false positive is WORSE than missing a real bug. An empty issues array is the ideal outcome for clean code.

**What to look for (in priority order):**
1. Bugs that WILL cause incorrect behavior — you must name the exact failing input
2. Security vulnerabilities — injection, XSS, exposed secrets, missing auth
3. Performance — N+1 queries, missing indexes, unnecessary re-renders
4. Standards — no inline \`style={{}}\` (use Tailwind), DRY violations, missing \`requireUser()\` in loaders/actions

**MANDATORY self-check — apply to EVERY potential issue before reporting:**
1. Can I name a SPECIFIC input that triggers a runtime failure? (If no → SKIP)
2. Does the code already handle this? Look for try/catch, null checks, \`??\`, \`?.\`, validation, mutation. (If yes → SKIP)
3. Have I read the FULL function body, not just the signature or call site? (If no → read it first)
4. Is this a style preference, design opinion, or "could be better" suggestion? (If yes → SKIP)
5. If I claim "line X runs before/after line Y" — have I re-read the diff to verify the actual line order? (If no → re-read it)

**Common false positive patterns — NEVER report these:**
- \`any\` types: intentional in this codebase for raw MongoDB data. Never flag.
- Unused return values: if a function mutates its input (e.g., \`obj.field = []\`), the caller does NOT need the return value. The object is already modified. This is NOT a bug.
  Example: \`sanitize(obj)\` where sanitize does \`obj.arr = obj.arr ?? []\` — the caller's \`obj\` is already fixed. Do not suggest assigning the return value.
- Misread execution order: if your issue claims code runs in a certain order, re-read the lines in the diff. Code runs top to bottom. Do not report bugs based on an incorrect reading of which line executes first.
- "Validation might be insufficient": unless you can prove a specific input passes the check AND causes a failure, do not report.
- Speculative language: if your description uses "may", "might", "could", "verify whether", "determine if", or "theoretically" — it is speculative. Do not report.
- Redundant hardening: do not suggest adding validation/types/error handling when the code already defends against the failure.
- Missing null checks on optional parent objects: if a parent is optional in the schema (\`Type?\`), its children don't need null-guarding when the parent is null.

**Rules:**
- State the EXACT input, the EXACT line that fails, and the EXACT consequence.
- If your issue involves execution order, quote the EXACT lines in sequence from the diff to prove your claim.
- Zero issues = best outcome. Do NOT invent issues to appear thorough.`;

    // Sanitize user-provided PR body to mitigate prompt injection.
    // PR_BODY comes from the PR author and is untrusted input.
    const sanitizedBody = (PR_BODY || "(no description)").slice(
        0,
        MAX_PR_BODY_LENGTH
    );

    const userPrompt = `## Pull Request #${prNumber}

**Title:** ${PR_TITLE || "(no title)"}
**Description (user-provided, may be unrelated to the actual diff):** ${sanitizedBody}
**Files changed:** ${totalFiles}${truncationNotice}

${diffContent}

Respond with a JSON object (no markdown fences, just raw JSON):
{
  "summary": "1-2 sentence overview of what was reviewed and how many issues were found. Issues only — no praise.",
  "issues": [
    {
      "path": "exact/file/path.ts",
      "line": 42,
      "severity": "HIGH|MEDIUM|LOW",
      "bug": "One-sentence description of a CONFIRMED bug (not a potential issue). Reference the exact problematic code with inline backticks and state what WILL break.",
      "suggestedFix": "Concrete description of how to fix the issue. Include corrected code if helpful.",
      "agentPrompt": "Multi-sentence explanation for an AI agent. Include: (1) the file and line, (2) what the code currently does wrong, (3) what the correct behavior should be, (4) why the current code produces incorrect results."
    }
  ]
}

Rules:
- \`path\` must exactly match a filename from the diff
- \`line\` must be a line number visible as an added (+) or context line in the diff
- \`severity\`: HIGH = bugs/security, MEDIUM = logic/performance, LOW = standards violations
- \`bug\` must quote the problematic code in backticks and state the consequence
- \`agentPrompt\` must be detailed enough for an AI agent to locate and verify the issue independently
- Maximum ${MAX_INLINE_COMMENTS} issues — prioritize by severity
- If no issues found, return \`"issues": []\`

Read the instructions again before responding:

CRITICAL: Only report CONFIRMED bugs, not POTENTIAL bugs. Every issue you report must be something that WILL fail, not something that MIGHT fail. If you cannot prove it breaks with a specific input, it is not a bug — do NOT report it. Reporting a false positive is WORSE than missing a real bug. An empty issues array is the ideal outcome for clean code.

**MANDATORY self-check — apply to EVERY potential issue before reporting:**
1. Can I name a SPECIFIC input that triggers a runtime failure? (If no → SKIP)
2. Does the code already handle this? Look for try/catch, null checks, \`??\`, \`?.\`, validation, mutation. (If yes → SKIP)
3. Have I read the FULL function body, not just the signature or call site? (If no → read it first)
4. Is this a style preference, design opinion, or "could be better" suggestion? (If yes → SKIP)
5. If I claim "line X runs before/after line Y" — have I re-read the diff to verify the actual line order? (If no → re-read it)

**Common false positive patterns — NEVER report these:**
- \`any\` types: intentional in this codebase for raw MongoDB data. Never flag.
- Unused return values: if a function mutates its input (e.g., \`obj.field = []\`), the caller does NOT need the return value. The object is already modified. This is NOT a bug.
  Example: \`sanitize(obj)\` where sanitize does \`obj.arr = obj.arr ?? []\` — the caller's \`obj\` is already fixed. Do not suggest assigning the return value.
- Misread execution order: if your issue claims code runs in a certain order, re-read the lines in the diff. Code runs top to bottom. Do not report bugs based on an incorrect reading of which line executes first.
- "Validation might be insufficient": unless you can prove a specific input passes the check AND causes a failure, do not report.
- Speculative language: if your description uses "may", "might", "could", "verify whether", "determine if", or "theoretically" — it is speculative. Do not report.
- Redundant hardening: do not suggest adding validation/types/error handling when the code already defends against the failure.
- Missing null checks on optional parent objects: if a parent is optional in the schema (\`Type?\`), its children don't need null-guarding when the parent is null.

**Rules:**
- State the EXACT input, the EXACT line that fails, and the EXACT consequence.
- If your issue involves execution order, quote the EXACT lines in sequence from the diff to prove your claim.
- Zero issues = best outcome. Do NOT invent issues to appear thorough.`;

    return { systemPrompt, userPrompt };
}

// --- Call Bedrock with retries ---

async function callBedrock(systemPrompt, userPrompt) {
    const requestBody = JSON.stringify({
        anthropic_version: "bedrock-2023-05-31",
        max_tokens: MAX_TOKENS,
        system: systemPrompt,
        messages: [{ role: "user", content: userPrompt }],
    });

    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
        try {
            const command = new InvokeModelCommand({
                modelId: MODEL_ID,
                contentType: "application/json",
                accept: "application/json",
                body: requestBody,
            });

            const controller = new AbortController();
            const timeout = setTimeout(
                () => controller.abort(),
                BEDROCK_TIMEOUT_MS
            );

            const response = await bedrock.send(command, {
                abortSignal: controller.signal,
            });
            clearTimeout(timeout);

            const responseBody = JSON.parse(new TextDecoder().decode(response.body));
            return responseBody.content[0].text;
        } catch (error) {
            const isThrottling =
                error.name === "ThrottlingException" ||
                error.name === "TooManyRequestsException" ||
                error.$metadata?.httpStatusCode === 429;

            if (isThrottling && attempt < MAX_RETRIES) {
                const delay = Math.pow(2, attempt) * 1000 + Math.random() * 1000;
                console.log(
                    `Bedrock throttled (attempt ${attempt}/${MAX_RETRIES}), retrying in ${Math.round(delay)}ms...`
                );
                await new Promise((r) => setTimeout(r, delay));
                continue;
            }

            throw error;
        }
    }
}

// --- Parse Claude response ---

function parseReviewResponse(text) {
    // Try to extract JSON from the response
    try {
        // First try direct JSON parse
        return JSON.parse(text);
    } catch {
        // Try to find JSON block in the text
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (jsonMatch) {
            try {
                return JSON.parse(jsonMatch[0]);
            } catch {
                // Fall through to plain text fallback
            }
        }
    }

    // Fallback: treat entire response as summary
    console.log("Could not parse JSON from Claude response, using as plain text");
    return {
        summary: text,
        issues: [],
    };
}

// --- Format issue comment body (Sentry Seer style) ---

function formatCommentBody(issue, index) {
    const refId = `${prNumber}/${index}`;

    let body = `**Bug:** ${issue.bug}\n`;
    body += `<sub>Severity: ${issue.severity || "MEDIUM"}</sub>\n`;
    body += `<!-- BUG_PREDICTION -->\n\n`;

    if (issue.suggestedFix) {
        body += `<details>\n`;
        body += `<summary><b title="Reference ID: \`${refId}\`">Suggested Fix</b></summary>\n\n`;
        body += `${issue.suggestedFix}\n`;
        body += `</details>\n\n`;
    }

    if (issue.agentPrompt) {
        body += `<details open>\n`;
        body += `<summary><b title="Reference ID: \`${refId}\`">Prompt for AI Agent</b></summary>\n\n`;
        body += "```\n";
        body += `Review the code at the location below. A potential bug has been identified by an AI\nagent.\n`;
        body += `Verify if this is a real issue. If it is, propose a fix; if not, explain why it's not\nvalid.\n\n`;
        body += `Location: ${issue.path}#L${issue.line}\n\n`;
        body += `Potential issue: ${issue.agentPrompt}\n`;
        body += "```\n";
        body += `</details>\n\n`;
    }

    body += `<!--\n<sub>Reference ID: \`${refId}\`</sub>-->`;

    return body;
}

// --- Map issues to diff positions ---

function mapIssuesToDiffPositions(issues, files) {
    const mapped = [];
    const unmapped = [];

    // Build position maps for all files
    const positionMaps = new Map();
    for (const file of files) {
        positionMaps.set(file.filename, buildLineToPositionMap(file.patch));
    }

    issues.forEach((issue, index) => {
        const posMap = positionMaps.get(issue.path);
        if (!posMap) {
            unmapped.push({ ...issue, _index: index });
            return;
        }

        const position = posMap.get(issue.line);
        if (!position) {
            unmapped.push({ ...issue, _index: index });
            return;
        }

        mapped.push({
            path: issue.path,
            position,
            body: formatCommentBody(issue, index),
        });
    });

    return { mapped: mapped.slice(0, MAX_INLINE_COMMENTS), unmapped };
}

// --- Resolve stale bot comments ---

async function resolveStaleComments(newIssues, dryRun = false) {
    // 1. Fetch all review comments on the PR (paginated)
    const allComments = [];
    let page = 1;

    while (page <= 10) {
        const { data } = await octokit.pulls.listReviewComments({
            owner: REPO_OWNER,
            repo: REPO_NAME,
            pull_number: prNumber,
            per_page: 100,
            page,
        });

        allComments.push(...data);
        if (data.length < 100) break;
        page++;
    }

    // 2. Filter to bot comments using the BUG_PREDICTION marker
    const botComments = allComments.filter(
        (c) => c.body && c.body.includes("<!-- BUG_PREDICTION -->")
    );

    if (botComments.length === 0) {
        console.log("No existing bot comments to resolve");
        return;
    }

    console.log(`Found ${botComments.length} existing bot comment(s)`);

    // 3. Build a Set of "path:line" keys from the new issues
    const newIssueKeys = new Set(
        newIssues.map((issue) => `${issue.path}:${issue.line}`)
    );

    // 4. Identify stale comments whose path:line is NOT in the new issues
    const staleComments = botComments.filter((comment) => {
        const line = comment.line || comment.original_line;
        const key = `${comment.path}:${line}`;
        return !newIssueKeys.has(key);
    });

    if (staleComments.length === 0) {
        console.log("No stale bot comments to resolve");
        return;
    }

    console.log(`Resolving ${staleComments.length} stale bot comment(s)...`);

    // 5. Minimize each stale comment via GraphQL (or log in dry-run mode)
    for (const comment of staleComments) {
        const line = comment.line || comment.original_line;

        if (dryRun) {
            console.log(`  Would resolve: ${comment.path}:${line} (node_id: ${comment.node_id})`);
            continue;
        }

        try {
            await octokit.graphql(
                `mutation($id: ID!, $classifier: ReportedContentClassifiers!) {
          minimizeComment(input: { subjectId: $id, classifier: $classifier }) {
            minimizedComment { isMinimized }
          }
        }`,
                {
                    id: comment.node_id,
                    classifier: "RESOLVED",
                }
            );
            console.log(`  Resolved: ${comment.path}:${line}`);
        } catch (err) {
            console.warn(
                `  Warning: failed to resolve comment ${comment.path}:${line}: ${err.message}`
            );
        }
    }
}

// --- Format the review body ---

function formatReviewBody(summary, totalIssues, mappedCount, unmappedIssues) {
    let body = `## AI Code Review\n\n${summary}\n`;

    if (totalIssues > 0) {
        body += `\n**${totalIssues} issue${totalIssues === 1 ? "" : "s"} found** (${mappedCount} inline, ${unmappedIssues.length} below)\n`;
    } else {
        body += `\nNo issues found.\n`;
    }

    if (unmappedIssues.length > 0) {
        body += `\n### Issues outside diff context\n\n`;
        body += `_These issues reference lines not in the diff and could not be placed inline:_\n\n`;
        for (const issue of unmappedIssues) {
            body += `---\n\n`;
            body += formatCommentBody(issue, issue._index);
            body += `\n\n`;
        }
    }

    body += `\n---\n_Review generated by ${MODEL_NAME} via AWS Bedrock_`;
    return body;
}

// --- Post error comment ---

async function postErrorComment(error) {
    const logsUrl = `${GITHUB_SERVER_URL || "https://github.com"}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}`;

    const body = `## AI Code Review - Error

The automated review encountered an error and could not complete.

**Error:** ${error.message || "Unknown error"}

[View workflow logs](${logsUrl})

---
_Review generated by ${MODEL_NAME} via AWS Bedrock_`;

    try {
        await octokit.issues.createComment({
            owner: REPO_OWNER,
            repo: REPO_NAME,
            issue_number: prNumber,
            body,
        });
    } catch (commentError) {
        console.error("Failed to post error comment:", commentError.message);
    }
}

// --- Set GitHub Actions output ---

function setOutput(name, value) {
    if (GITHUB_OUTPUT) {
        const delimiter = `ghadelimiter_${Date.now()}`;
        appendFileSync(
            GITHUB_OUTPUT,
            `${name}<<${delimiter}\n${value}\n${delimiter}\n`
        );
    }
}

// --- Main ---

async function main() {
    console.log(`Reviewing PR #${prNumber} in ${REPO_OWNER}/${REPO_NAME} (model: ${MODEL_NAME})`);

    // 1. Fetch PR files
    console.log("Fetching PR files...");
    const allFiles = await fetchPRFiles();
    console.log(`Found ${allFiles.length} changed files`);

    if (allFiles.length === 0) {
        console.log("No files changed, skipping review");
        return;
    }

    // 2. Prepare diff content
    const { files, truncated, totalFiles } = prepareDiffContent(allFiles);
    console.log(
        `Prepared ${files.length} files for review${truncated ? " (truncated)" : ""}`
    );

    // 3. Build prompt
    const { systemPrompt, userPrompt } = buildPrompt(
        files,
        truncated,
        totalFiles
    );

    // 4. Call Bedrock
    console.log("Calling Claude via Bedrock...");
    const responseText = await callBedrock(systemPrompt, userPrompt);
    console.log("Received response from Claude");

    // 5. Parse response
    const review = parseReviewResponse(responseText);
    const summary = review.summary || "No issues found.";
    // Support both "issues" (new format) and "comments" (legacy fallback)
    const issues = review.issues || review.comments || [];

    console.log(`Parsed: ${issues.length} issues found`);

    // 6. Resolve stale bot comments from previous runs
    await resolveStaleComments(issues, isDryRun);

    // 7. Map issues to diff positions
    const { mapped, unmapped } = mapIssuesToDiffPositions(issues, files);
    console.log(
        `Mapped ${mapped.length} issues to diff positions, ${unmapped.length} could not be mapped`
    );

    // 8. Format review body
    const reviewBody = formatReviewBody(
        summary,
        issues.length,
        mapped.length,
        unmapped
    );

    // 9. Submit review or dry-run
    if (isDryRun) {
        console.log("\n=== DRY RUN — Review would be: ===\n");
        console.log(reviewBody);
        if (mapped.length > 0) {
            console.log("\n=== Inline comments: ===\n");
            for (const c of mapped) {
                console.log(`  ${c.path} (pos ${c.position}): ${c.body}`);
            }
        }
    } else {
        console.log("Submitting review...");
        await octokit.pulls.createReview({
            owner: REPO_OWNER,
            repo: REPO_NAME,
            pull_number: prNumber,
            event: "COMMENT",
            body: reviewBody,
            comments: mapped,
        });
        console.log("Review submitted successfully");
    }

    // 10. Set step output
    setOutput("summary", summary);
}

main().catch(async (error) => {
    console.error("AI review failed:", error);
    if (!isDryRun) {
        await postErrorComment(error);
    }
    process.exit(1);
});