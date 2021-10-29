import os
from pathlib import Path
import shutil


for path_, dirs, files in os.walk("."):
    path = Path(path_)
    try:
        i_pycache = dirs.index("__pycache__")
        shutil.rmtree(str(path / "__pycache__"))
        del dirs[i_pycache]
    except ValueError:
        pass
        
    for file_ in files:
        file = path / file_
        ext = file.suffix
        if any(ext.endswith(x) for x in ["pyo", "pyc"]):
            file.unlink()
            
for p in Path(".").glob(".make.*"):
    p.unlink()
