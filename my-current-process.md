# Current Process 2026-01-22

1. original planning this is just talking to opus with just your feature idea and goal in mind. If you have the input data format and output data format give it that as well.
    1. Make sure to mention you want to follow TDD (Test Driven Development). 
    1. Ask it if it has any questions about any of your plan or test env that you need to clarify.
    1. In that same context when you believe it understands the feature plan use /plan-feature to get it to create the correct formatted plan.md file.
    1. manually review the process. (Sometimes depending on complexity of feature, ask a new context to critique your plan asking you questions about it and the goals.)
1. New context run /implement-plan plan.md (Normally run /prime before /implement-plan just not this time)
    1. Watch what it is doing it is normally good about staying on plan but it is a newer rendition of this command so might need some work on my end. Let me know if it does anything crazy. (Maybe put it as an issue in github for my py-starter repo if it seems serious.)
    1. Make sure all tests it created pass.
    1. Manually review normally running the server and making sure everything is still working as it should. (Might want a checklist of things you check everytime you change a feature that would really break something or change analysis.)
 
1. New context /prime then /code-review
    1. Fix the things that might be critical errors from its findings in this context window.
    1. manual review like step 3 above.
    1. Commit
1. Repeat for each feature
1. When going to push to main branch make sure to run /prime then /code-review-since <commit_code> or <dev/main> the one that you branched from