# Stage 1: Start


* (NAMING-ZOO): File and function names are indiscipherable and difficult to parse.

* **Share contributor guidelines**: Sometimes, the first time I land on a GitHub repo is because I found a bug in the code and I'm looking to submit an issue. It's nice to know what my first step as someone who wants to be friendly as a developer should do to report a bug, or even to debug the issue myself and submit at PR. It's great when there's instructions on what to report, which tests to run, and how I can best help the maintainers in helping me.

# Stage 2:

* **Name things to find them later**: It doesn't matter how good your work is, if it's impossible to read, no one can understand it. Use names that are both machine readable (no weird characters) and human understandable. Take an extra second to make the name of your files, functions and really anything you have to name be simple, short, intuitive. If you come looking for it later, and don't find it on your first guess, rename it. Now. Pro-tip: rename it what you looked for first!

# Stage 3: Env

* (HARDCODED-PATH) A file contains a hardcoded path, so the project will not run elsewhere without manual editing


* **Always use relative paths** All paths that you use in your code should be relative paths and not hardcoded.

## Local Paths

Easydata makes all paths relative to the base project path using the `Pathlib` library and a local configuration file: `catalog/config.ini `. By the way, `Pathlib` is also an awesome way to manage paths across platforms.

from src import paths
paths

Modify the `catalog/config.ini` to include the path to our `quest` directory. That is, we want `paths['quest_path']` to be

paths['project_path'] / 'quest'

# Stage 5: Test
* (EYEBALL-TEST) Only way to check if I got the same results was to compare against outputs in the original notebook and images (but the images didn't match because of randomness)

* **RANDOMNESS**
    * (NO-PRNG-SEED) No fixed random seed was used, or there was no option to use one
    * (PRNG-FAIL) Code has a fixed pseudo-random seed, but results are still not reproducible
    * (UNLUCKY-SEED) A certain choice of random seed results in unexpected or pathological behavior; e.g. infinite loop
    * (NONDETERMINISTIC) Behavior cannot be modeled or reproduced. (e.g. True Randomness)

* **Keep track of your random seeds**: Many algorithms aren't deterministic. Keep track of your random seeds whenever possible so you can control as much randomness as you can.
* **Save a copy of your output (images)**: While eyeball tests aren't ideal as the only check, it's sometimes the only way to check if you've controlled for randomness and successfully reproduced a results. Save your output images. Many a time have we found architecture differences from pictures! Check-in your `Kernel -> Restart & Run All` Notebooks (`nbdiff` is your friend here!)

# Stage 6: Story

## Reproducibility Issues
* (DOCUMENTATION-BUGS): A documentation bug is an error in documentation or missing documentation. Missing documentation is any explanation in prose form that you're looking for but can't find.
    * (NO-DOCSTRINGS): Functions without docstrings, a subcategory of documentation bugs.
* (THE-KITCHEN-SINK): Code and prose are mixed in a monolithic notebook. Utility scripts are mixed into the main narrative. Everything's in that notebook, including the kitchen sink.
* (TL;DR): Documentation and/or code is too long and confusing. Get to the point. Every joke needs a punch line. Every story needs a climax. Every repo needs a raison d'etre.
* (HARD-TO-FOLLOW): Everything is technically there. But it's hard to figure out how to piece it all together. What needs to be run first? What order do things need to be run in? Is it a quest to figure out the next step?
    * (NO-NOTEBOOK-ORDER): This is a special instance of HARD-TO-FOLLOW that we like to highlight. What order do the notebooks need to be run in? Do they depend on each other? If so, is the dependency indicated in the names?

### Default Better Principles

* **Keep the prose close to the code**: Keep the explanation of what something does right next to it.
    * **Use Python Docstrings**: In Python, all functions should have docstrings. It reflects their higher calling. Hitting `Shift-Tab` from a notebook makes it easy to figure out what a function is supposed to be doing right there, in a moment. A function without a docstring is naked. Help the functions stay decent.
    * **Tell stories with Jupyter Notebooks**: Mix code and prose using Notebooks. They are fantastic for interweaving code and prose.
* **Use a Notebook naming convention**: Indicate what order to run notebooks in

* **Remove everything that's not essential to the story**:
    * **Automate your workflow**: Automate any task you do repeatedly.
    * **Put helper and utility functions in modules**: Ruthlessly take code out of your notebooks and put it into modules
* **Cut-cut-cut. Iterate.**: Remove everything that's not essential to the story. Put helper and utility functions in modules. Ruthlessly take code out of your notebooks and put it into modules.
