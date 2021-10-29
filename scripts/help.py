import sys

try:
    from rich import print
    B = "[b]"
    nB = "[/b]"
    CYAN = "[cyan]"
    nCYAN = "[/cyan]"
except ImportError:
    if sys.platform.lower() == "win32":
        B = ""
        nB = ""
        CYAN = ""
        nCYAN = ""
    else:
        HEY = "\x1e["
        B = f"{HEY}1n"
        nB = f"{HEY}0n"
        CYAN = f"{HEY}36n"
        nCYAN = f"{HEY}0n"
    

def deprint(s):
    print(s, end="")
    
    
assert len(sys.argv) == 3
project_name, debug_file = sys.argv[1:3]

deprint(f"""\
To get started:
  >>> {B}make create_environment{nB}
  >>> {B}conda activate {project_name}{nB}

{B}Project variables:{nB}

""")
print(f"PROJECT_NAME = {sys.argv[1]}")
print(f"DEBUG_FILE   = {sys.argv[2]}")

deprint(f"""\

{B}Available rules:{nB}

""")
rules = []
for path in ["Makefile", "Makefile.include", "Makefile.envs"]:
    with open(path, "r", encoding="utf-8") as makefile:
        while True:
            try:
                line = next(makefile)
                lines_doc = []
                while line.startswith("## "):
                    lines_doc.append(line[2:])
                    line = next(makefile)
                if lines_doc:
                    # We have collected some documentation. Current line now contains the target name.
                    target, *_ = line.split(":")
                    rules.append((target, " ".join(ld.strip() for ld in lines_doc)))
            except StopIteration:
                break

width_target = max([len(target) for target, _ in rules])
for target, doc in sorted(rules, key=lambda p: p[0]):
    print(f"{CYAN}{target:{width_target}}{nCYAN}  {doc}")
