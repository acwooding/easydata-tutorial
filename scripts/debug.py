import os
from subprocess import run, STDOUT
import sys


assert len(sys.argv) >= 2
path_debug = sys.argv[1]

with open(path_debug, "wb") as file_debug:
    def shell_out(*cmd):
        return run(list(cmd), stdout=file_debug, stderr=STDOUT, input=b"yes\n")

    def heading(h):
        file_debug.write(bytes(f"\n##\n## {h}\n##\n", encoding="utf-8"))
        file_debug.flush()

    heading("Git status")
    shell_out("git", "status")

    heading("git log")
    shell_out("git", "log", "-8", "--graph", "--oneline", "--decorate", "--all")
    
    heading("Git remotes")
    shell_out("git", "remote", "-v")
    
    heading("GitHub SSH credentials")
    shell_out("ssh", "git@github.com")
    
    heading("Conda config")
    shell_out(os.environ["CONDA_EXE"], "config", "--get")
    
    heading("Conda info")
    shell_out(os.environ["CONDA_EXE"], "info")
    
    heading("Conda list")
    shell_out(os.environ["CONDA_EXE"], "list")

msg = f"Please include the contents of {path_debug} when submitting an issue or support request."
print("=" * len(msg))
print(msg)
print("=" * len(msg))