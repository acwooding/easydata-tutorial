# Step-by-step WSL install on Windows
​We've found that things work best using Windows Subsystme for Linux. While you can use other shells, we recommend using this one to make your life easier.

Our order of operations would be:
* Install WSL
* Install miniconda
* Make sure git was installed
* Install `make` via `conda install make`

## Install and set up Windows Subsystem for Linux

** Install Windows Subsystem for Linux (WSL) on Windows 10
https://docs.microsoft.com/en-us/windows/wsl/install

Note the default install is Ubuntu by there are instructions in the link for other distros.

For older versions of Windows 10:
https://docs.microsoft.com/en-us/windows/wsl/install-manual

** Best practices for setting up WSL
https://docs.microsoft.com/en-us/windows/wsl/setup/environment

This includes useful tips on setting up Git, VS Code, and other helpful things.

## Install miniconda on WSL if not present

** Get the Linux miniconda install file for the version you want:
It's easiest to just install via Windows to your normal download directory.
https://docs.conda.io/en/latest/miniconda.html#linux-installers


** Open a terminal for Windows Subsytem for Linux (WSL)
You can follow the instructions in the best practices link above to set up Windows Terminal, or just type `wsl` at a Windows command line.

** Launch the Miniconda installers
Note that your Windows drives/folders are available at `/mnt/c/Users/<userid>`.

Navigate to your Windows download folder and run the installer.  Example:
```
cd /mnt/c/Users/<userid>/Downloads

bash Miniconda3-py38_4.10.3-Linux-x86_64.sh
```

Accept the terms and start the install.

Optional: Agree to initialize with conda with conda init.

Close the terminal, open a fresh WSL terminal and confirm that minicona is installed:
```which conda```

## Setup ssh and install the repo

** Ensure you have Git on WSL
Git should be preinstalled.  If there is an issue, instructions are here:
https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-git

** Setup an ssh key for WSL and add it to your Github
Generate a new key in WSL terminal:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Add the new key to your Github account:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
