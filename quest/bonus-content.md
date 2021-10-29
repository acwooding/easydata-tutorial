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