from src.data import Dataset
from src.utils import run_notebook
from src import paths

# Check the umap import
import umap

# Check the datasets load
ds = Dataset.load('penguins-clean')
assert ds.data.shape == (334, 7)

ds = Dataset.load('penguins-scaled')
assert len(ds.data) == 334

# Test that the notebook runs to completion
path_test_runs = paths["notebook_path"] / "test-runs"
path_test_runs.mkdir(parents=True, exist_ok=True)
run_notebook(notebook_name="05-Testing-Challenge.ipynb",
             notebook_path=paths['notebook_path'],
             output_notebook_name="05-Testing-Challenge-Test-Run.ipynb",
             output_notebook_path=path_test_runs)

print("""\n
***************************

Challenge notebook complete. Head over to

https://amy105172.typeform.com/quest-test

to complete this Stage of the Quest.

***************************

""")
