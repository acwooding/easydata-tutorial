# The Easydata Git Workflow
Here's our suggestion for a reliable git workflow that works well in small team settings using [Easydata][cookiecutter-easydata].

## Git configuration

If you haven't yet done so, please follow the instrucitons
in our [Git Configuration Guide](git-configuration.md) first.

## Git Workflow

We suggest you start each day by doing this:

### Where was I? What was I doing? Did I check it in?
Sometimes, you stop work without checking things back in to the repo.
Now, before you do any additional work, is the time to fix that.
```bash
git branch   # what branch am I on?
git status   # are there any files that need checking in?
git add -p   # accept or reject parts of the modified files
git commit -m "put your commit message here"
```

### Did I do any work elsewhere?
Did you make changes to your personal fork, but on a different machine? Make sure your local branch is up-to-date with your personal fork (`origin`):
```bash
git checkout main
git fetch origin --prune
git merge origin/main
```

### What happened upstream?
Did someone make changes to the `upstream` repo in your absense?
Let's fetch and merge those changes

```bash
git checkout main
git fetch upstream --prune
git merge upstream/main
git push origin main
make update_environment
```

### Am I working from the latest `main`?
Now that your `main` branch is up-to-date with both `origin` and `upstream`, you should use it to update your local working branches. If you are already developing in a branch called, e.g. `my_branch`, do this before writing any more code:

```bash
git checkout my_branch
git merge main
git push origin my_branch
```

### Do I have any stale branches?
With your local `main`, `origin/main` and `upstream/main` all in sync, we like to clean up any old branches that are fully merged (and hence, can be deleted without data loss.)
```bash
git branch --merged main
git branch -d <name_of_merged_branch>
```
A really great feature of `git branch -d` is that it will refuse to remove a branch that hasn't been fully merged into another. Thus it's safe to use without any fear of data loss.


### Time to start the day
Once you've finished all your merge tasks, you can create a clean working branch from the latest `main` by doing a:
```bash
git checkout main
git checkout -b new_branch_name
```


That's it!

**Next stop**: explore the default Easydata project organization at the bottom of the `README.md` for this repo. Ok. So it's not quite default. Your quest instructions didn't come with the default. But let's not get too pedantic here.


Do you have any suggestions for improvements to this workflow? Drop us a line or file an issue at
[cookiecutter-easydata].

[cookiecutter-easydata]: https://github.com/hackalog/cookiecutter-easydata/