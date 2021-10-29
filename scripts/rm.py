from pathlib import Path
import shutil
import sys


for pattern in sys.argv[1:]:
    for path in Path(".").glob(pattern):
        if path.is_dir():
            shutil.rmtree(str(path))
        else:
            path.unlink()
