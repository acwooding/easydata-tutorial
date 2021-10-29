# Stage 1: Where do I start?

At the very beginning of everything is, well, the beginning. If I can't find an accessible place to start, no matter how wonderful or worthwhile someone's work is, and no matter how committed I am, I won't make it past the start line. TL;DR.

We have conventions that dictate where to start. Like saying "Hello". In the code world, a [README] (or README.md) file is your way to say "Hello". In fact, on GitHub, you don't even have to remember this the README.md file displays up front when you open the URL for a repo (same with GitLab or Bitbucket, but for simplicity throughout we'll simply refer to GitHub).

The [README] is your chance to say something lik:

* Welcome! Please come in.
* Danger! We're actively undergoing major construction, put on your hard hat and help us out.
* Do not Enter! No Trespassing. Stay away. Don't bother looking at what's here.

If you haven't taken a look at the [README.md][README] file for this repo yet, **now is the time**. Please do so and follow the instructions to make sure your basic setup is complete. The [README] is the place to start before continuing on any Quest for Reproducibility.

[README]: https://github.com/acwooding/easydata-tutorial/blob/main/README.md

Now, for our first handful of reproducibility issues.

### Reproducibility Issues
* (NO-README): There is no README file. Enough said.
* (WHERE-DO-I-START): The README doesn't say where to start. Or indicate basic dependencies.
* (NO-CODE-LICENSE): No license on source code.
* (NAMING-ZOO): File and function names are indiscipherable and difficult to parse.

## The Easydata Way

The Easydata way to indicate the start line is the "simple, sleep-deprived, I don't have to think about it way". Whenever possible, make where and how to start as easy and frictionless as possible. In particular:

### Default Better Principles
* **Give starting instructions in a README**: Welcome your users. Include:
  * **A basic description**: what can they expect? Is this a finished project, a work in progress (WIP), a place to dump your code that you don't want anyone to look in (like your underwear drawer)?
  * **Instructions for what to install**: Let people know what dependencies are required and how to get started by letting them know what you use: a `requirements.txt` file, and `environment.yml` (which we'll see later). Also, if you only support certain platforms/architectures, it's nice to let folks know before they try to set up and fail that you don't their compute setup.
  * **The next step**: Include what you expect someone to do next once they finish reading the README.
* **Add a code license**: We especially like stardard open-source licenses like the default options in GitHub. Without a license, the default in many places is that your work is copywrited and proprietary if there is no license. And even if your work is proprietary, say so. Failing to license your work is the easiest way to hang a "DO NOT ENTER" sign accidentally.
* **Share contributor guidelines**: Sometimes, the first time I land on a GitHub repo is because I found a bug in the code and I'm looking to submit an issue. It's nice to know what my first step as someone who wants to be friendly as a developer should do to report a bug, or even to debug the issue myself and submit at PR. It's great when there's instructions on what to report, which tests to run, and how I can best help the maintainers in helping me.

When you create an Easydata repo, we get you started and make sure that you don't forget to include your welcome. By default, setting up an Easydata repo prompts you for a:

* Project Name
* Project Description
* Author Name
* Open-source License

and generates a `README.md` file and `LICENSE` file from your answers.

Now that you've started, take a look at the auto-generated [LICENSE] for this project to find out what you're allowed to do with the contents of this repo, and to continue on your quest.

[LICENSE]: https://github.com/acwooding/easydata-tutorial/blob/main/LICENSE

## Deep Dive References
Want to explore this theme more? Here are some references:

### Welcoming

* Design

### Open-source Licenses
