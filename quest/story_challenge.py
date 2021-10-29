from src.quest import quest_instruction
from src.utils import run_notebook
from src import paths

assert quest_instruction.__doc__ != None
run_notebook(notebook_name="06-Story-Challenge.ipynb",
     notebook_path=paths['notebook_path'],
     output_notebook_name="06-Story-Challenge-Test-Run.ipynb",
     output_notebook_path=notebook_test_path)


print("""\n
******************************************************

Challenge notebook complete. Head over to

https://amy105172.typeform.com/quest-story

to complete this Stage of the Quest.

******************************************************

""")
