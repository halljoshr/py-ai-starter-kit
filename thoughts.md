- I think that somethinhg I want to explore is the flow of how we want this whole thing to work. Like I want to be heavily involved at the start of any feature or whatever but then I do not want to have to babysit the model and tell it about the errors in the code it should be able to find those by running effectively. And testing.
- I probably want to use some drawing tools for different functionalities. We defintely want to predefine what the data looks like.
- We should have small examples that actually pull and deal with data on their own so that the agent knows exactly how to get it, process it and what the output should look like without guessing.
- We certainly want to work in the smart section of the context window pre 120k tokens. Reset this often.
- Work from specs so that things can be reviewed and broken down into stupid simple tasks. I think even less things than we think.
- Dynamic teaching of the context of our large codebases is important because current prime wastes all of the smart context.
- should know to kill any sub process it starts as a cleanup feature to not block other agents or me from testing.
- Probably needs an orcastrator agent at some level and then other sub agents that specialize in one thing and does them well. Like code review or code docs for finding what we need to give as context for the specific feature.
- I said this before but it should always attempt to run it as a server if applies so that it can monitor for the errors that I am just going to copy paste into the context.
- Completely remove the timing aspect of context. I do not care how long you think it will take a human to do it. We ship 50k lines in a weekend sometimes. Those are the off days!
- Havew metrics that mean something for how much we are getting done. This can be related to tickets but also about building code right the first time that generally doesnt change unless there is a change in philosophy.
- Have a good documentation system where we can show exactly how we got to a stage with all of the commands and the context that was used to build the next thing.
- Have conversations early with AI and have team members review the ideas instead of the code review. We should put these out for pretty much every feature.
- Tool definitions and SOPs for how we do certain things. Both within the coding agents but also what external tools we always use. Linear, Sentry, AWS etc.
- Knowing how data is accessed and its schemas
- Strict rules on what it should look like schema and data wise for testing. The amount of times we change code and they break something that was already working is so high. Like it should now from the test cases that there is revenue in deal XXX for year Y and if it doesn't see it then we know something broke.
- Should have someone read our PRs even though most of the convo should be in the research and planning stages.
- utilize skills as much as possible with their yaml descriptions.
- We should always have code review run before we say a feature is built and working.
- Then we should always have some form of optimization of our process once we know it is doing what it is supposed to.
- On top of that part of any data project should be understanding the scope of how much data is going to come through and therefore build a at scale test with faker data that is mapped the same way as our real data will be based on the specs and we should test the dependability and scaleability of our code and data. Know our limitations.
- Build all agents and skills as platform agnostic. We are about the idea not the team that is currently in the lead.
- Alway cache data that we want to test with. Then always have a subset of data that we have run through it but is not saved as a validation layer.
- Always have your code validated by the strictest standards we use. Otherwise I refactor way too much like this project.
- if the AI gets stuck in some loop of failure it should document it and stop so we do not waste tokens. Then maybe it should message us in some way so we know to look at it.
- We should self police with the AI by looking at the messages that we send the AI and figure out what category they live in so that we can improve the interactions. Like we want back and forth in research but not in implementation. Lets figure that out.
- Optimize models but I think research should be opus and updates haiku and implementation sonnet or something along those lines. Always have true metric for your output like you are a better engineer if you use less tokens for the same output as long as you are just as fast or you time is worth less than the differnce in the speed. DO THIS FOR REAL!
- Try to build code into all skills and agents that could benefit from them instead of depending on markdown that has to be interpretted.
- Daily output report to show what you got done in terms of tickets and coding and research.
- iterating on the workflow after every project. Ask what could have been done better. Look at your metrics.
- Make sure we are logging nicely.
- Make sure that we are logging how it went in the moment for each feature, but, ticket, or project. Real stats.
- Make sure we have an auditable log of data that gets sent to agents and is received from them. So we can recreate scenarios.
- Make sure GH Actions do not take an hour to run simple tests.
- Make sure that we have self deployment techniques and have them logged in the SOPs


# Added after orginal critque
- I want to stop having to say this all of the time when getting coverage correct for pytest. This should be in a skill or something. This one too. "please do not run the full test suite just look at the coverage on a file by file basis when you change one and see how many lines you moved from miss to hit."
- My response to vague is that it depends on each skill how much we have to code and what language we are not restricted to python we can use rust, go, or cpp if necessary to test things. Whatever is best for what we are doing. As long as it fits in our ecosystem.
- Just watched someone use hooks as a way to run code like type check etc after claude thinks it is done but in reality it is not done. So we could do something like this where it would start the server make sure there are no errors then run the ruff and mypy and pytest etc from this sort of setup.
- I am really talking about mermaid as our diagram stuff
- If you go to far away from where I want and I cannot get you back on track in one prompt we should revert the code base and drop that exprot of the conversation into one of the super powerful deepthink models to try and find a better way to get it to go in our direction.
- What is the standard claude planning mode? Is what we are building objectively better?
- I think we are gettin to dependent on claude as well we forgot about the maker model as well. We want to use multiple models and get them voting on a system. So how do we do that effectively with creating code?

Project where we look at building a HubSpot module in Python to see if we can send in a deal ID or pre-screen ID any kind of ID to get the HubSpot deals or businesses. I want it to be a module that I can plug and play into any of the future tools that we build for this workflow.Okay, can you set the default time to five minutes and then can you test this using Honcho and make sure that we test it with the deal that already has the personal tax and business tax?DI






What would it take for us to turn this into a desktop UI of some sort so the non-technical people could also use this tool?

Can we refactor this so that it actually looks like a good Python project following all the rules that we would if you were building this from scratch? Look at our PIV model for that.