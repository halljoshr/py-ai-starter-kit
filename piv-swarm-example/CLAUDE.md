# CLAUDE.md - Todo API

Simple FastAPI Todo API for testing PIV-Swarm workflow.

## Project Overview

A basic REST API for managing todo items.

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- pytest

## Code Standards

- Line length: 100
- Type hints required
- Tests required for all features

## Commands

```bash
# Run server
uv run uvicorn src.main:app --reload

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy src/
```

## Directory Structure

```
src/
├── main.py          # FastAPI app
├── api/             # Route handlers
├── models/          # Pydantic models
└── services/        # Business logic

tests/
├── unit/            # Unit tests
└── integration/     # API tests
```
