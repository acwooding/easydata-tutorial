from src.data import Dataset
from src.utils import run_notebook
from src import paths


# Check the datasets load
ds = Dataset.load('penguins-clean')
assert ds.data.shape == (334, 7)

ds = Dataset.load('penguins-scaled')
assert len(ds.data) == 334

# Test that the notebook runs to completion
run_notebook(notebook_name="04-Data-Challenge.ipynb",
             notebook_path=paths['notebook_path'],
             output_notebook_name="04-Testing-Challenge-Test-Run.ipynb",
             output_notebook_path=paths['notebook_path'] / "test-runs")

print("""\n
***************************

Challenge notebook complete. Head over to XXXXtypeform to complete this Stage of the Quest.

***************************

""")
