#
# GLOBALS                                                                       #
#
include Makefile.include

#
# Manage Environment
#

include Makefile.envs

#
# Deprecated
#

.PHONY: requirements

requirements: update_environment
	@echo "WARNING: 'make requirements' is deprecated. Use 'make update_environment'"

.PHONY: unfinished
unfinished:
	@echo "WARNING: this target is unfinished and may be removed or changed dramatically in future releases"

#
# COMMANDS                                                                      #
#



.PHONY: begin
begin:
	python quest/begin.py

.PHONY: repo_challenge
repo_challenge:
	python quest/repo_challenge.py

.PHONY: data_challenge
data_challenge:
	python quest/data_challenge.py

.PHONY: test_challenge
test_challenge:
	python quest/test_challenge.py

.PHONY: env_challenge
env_challenge:
	python quest/env_challenge.py

.PHONY: story_challenge
## **Quest Task**: When you've completed notebook 06, run this command!
story_challenge:
	python quest/story_challenge.py

.PHONY: complete_challenge
## Complete the full Quest
complete_challenge: repo_challenge data_challenge test_challenge env_challenge story_challenge
	python quest/complete_challenge.py

.PHONY: data
data: datasets

.PHONY: raw
raw: datasources

.PHONY: datasources
datasources: .make.datasources

.make.datasources: catalog/datasources/*
	$(PYTHON_INTERPRETER) -m $(MODULE_NAME).workflow datasources
	#touch .make.datasources

.PHONY: datasets
datasets: .make.datasets

.make.datasets: catalog/datasets/* catalog/transformers/*
	$(PYTHON_INTERPRETER) -m $(MODULE_NAME).workflow datasets
	#touch .make.datasets

.PHONY: clean
## Delete all compiled Python files
clean:
	$(PYTHON_INTERPRETER) scripts/clean.py

.PHONY: clean_interim
clean_interim:
	$(call rm,data/interim/*)

.PHONY: clean_raw
clean_raw:
	$(call rm,data/raw/*)

.PHONY: clean_processed
clean_processed:
	$(call rm,data/processed/*)

.PHONY: clean_workflow
clean_workflow:
	$(call rm,catalog/datasources.json)
	$(call rm,catalog/transformer_list.json)
.PHONY: test

## Run all Unit Tests
test: update_environment
	LOGLEVEL=DEBUG pytest --pyargs --doctest-modules --doctest-continue-on-failure --verbose \
		$(if $(CI_RUNNING),--ignore=$(TESTS_NO_CI)) \
		$(MODULE_NAME)

## Run all Unit Tests with coverage
test_with_coverage: update_environment
	coverage run -m pytest --pyargs --doctest-modules --doctest-continue-on-failure --verbose \
		$(if $(CI_RUNNING),--ignore=$(TESTS_NO_CI)) \
		$(MODULE_NAME)

.PHONY: lint
## Lint using flake8
lint:
	flake8 $(MODULE_NAME)

.phony: help_update_easydata
help_update_easydata:
	python scripts/help-update.py

.PHONY: debug
## dump useful debugging information to $(DEBUG_FILE)
debug:
	@python scripts/debug.py $(DEBUG_FILE)


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help
.PHONY: show-help
show-help:
	@python scripts/help.py $(PROJECT_NAME) $(DEBUG_FILE)
