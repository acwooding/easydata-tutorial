## A lot to remember? Here's your Quest cheat sheet.

If that all seems like a lot to keep track of and implement, well, it can be. But you don't have to do all of the work yourself. We created Easydata because we wanted to make reproducibility easy to do, by default, without having to think about it. And if there's ever anything we forget or need to look up regularly, we include it in the documentation, so reminders on how to do things reproducibly are right there, with every Easydata generated repo.

All in all, here's how you can make your work reproducible using Easydata:

1. **Where to start?**
    * Start with an Easydata repo template
    * Connect it with a GitHub repo (or GitLab, BitBucket etc.)

2. **Where to go next?**
    * Use a collaborative git workflow to keep track of work. A cheat sheet comes with the repo.
    * Create a map: an intuitive, documented project structure, with clear names. Thankfully, it's built in to Easydata!
3. **What to install?**
    * `make` environment management with `conda` easy via the `environment.yml` and lock file
    * Keep paths relative using `src.paths`
4. **Where to get the data?**
    * Create `Dataset` recipes to manage your data flow, metdata, and provenance
    * Easily access your data via `Dataset.load()`
5. **Does it work as expected?**
    * `Kernel -> Restart & Run All` or `from src.utils import run_notebook` before sharing/checking in notebooks
    * Always `make test` and use CI where possible
    * Keep track of your random seeds
    * Save your image results
6. **What's the point?**
    * Use Notebooks, the autodocumenting `Makefile` and the `src` module to combine code with your story


Of course, these are our opinions and our choices. Maybe they won't all suit you, and that's when you can drop down the rabbit hole to the level of the reproducibility principles behind it. Maybe you'll even disagree with one of these principles. The framework is flexible, so make your own choices, adapt it, `make` it your own and let us know what you've done along the way so we can iterate and make what we do better, together. We're always iterating, simplifying and cut-cut-cutting. We appreciate feedback and contributions along the way.

Finally, last of all, to complete the Easydata Quest for Reproducibility `make complete_quest`.