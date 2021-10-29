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
	python make_scripts/begin.py


.PHONY: env_challenge
begin:
	python quest/env_challenge.py

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
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -f .make.*

.PHONY: clean_interim
clean_interim:
	rm -rf data/interim/*

.PHONY: clean_raw
clean_raw:
	rm -f data/raw/*

.PHONY: clean_processed
clean_processed:
	rm -f data/processed/*

.PHONY: clean_workflow
clean_workflow:
	rm -f catalog/datasources.json
	rm -f catalog/transformer_list.json
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
# Lint using flake8
lint:
	flake8 $(MODULE_NAME)

.phony: help_update_easydata
help_update_easydata:
	@echo "\nTo update easydata on an existing repo, verify that you have an 'easydata' branch"
	@echo "\n>>>git rev-parse -q --verify easydata"
	@echo "\nIf no output is given, do this:"
	@echo "\n>>>git branch easydata `git rev-list --max-parents=0 HEAD`"
	@echo "\nIf no output is given, do this:"
	@echo "\nCheck-in all your changes, then merge the new easydata branch into yours"
	@echo "\ngit branch easydata"
	@echo "# replace easydata with https://github.com/hackalog/easydata if needed"
	@echo "pushd .. && cookiecutter --config-file $(PROJECT_NAME)/.easydata.yml easydata -f --no-input && popd"
	@echo "git add -p  # add all the changes"
	@echo "git commit -m 'sync with easydata'"
	@echo "git checkout main"
	@echo "git merge easydata"

.PHONY: debug
## dump useful debugging information to $(DEBUG_FILE)
debug:
	@echo "\n\n======================"
	@echo "\nPlease include the contents $(DEBUG_FILE) when submitting an issue or support request.\n"
	@echo "======================\n\n"
	@echo "##\n## Git status\n##\n" > $(DEBUG_FILE)
	git status >> $(DEBUG_FILE)
	@echo "\n##\n## git log\n##\n" >> $(DEBUG_FILE)
	git log -8 --graph --oneline --decorate --all >> $(DEBUG_FILE)
	@echo "\n##\n## Github remotes\n##\n" >> $(DEBUG_FILE)
	git remote -v >> $(DEBUG_FILE)
	@echo "\n##\n## github SSH credentials\n##\n" >> $(DEBUG_FILE)
	ssh git@github.com 2>&1 | cat >> $(DEBUG_FILE)
	@echo "\n##\n## Conda config\n##\n" >> $(DEBUG_FILE)
	$(CONDA_EXE) config --get >> $(DEBUG_FILE)
	@echo "\n##\n## Conda info\n##\n" >> $(DEBUG_FILE)
	$(CONDA_EXE) info  >> $(DEBUG_FILE)
	@echo "\n##\n## Conda list\n##\n" >> $(DEBUG_FILE)
	$(CONDA_EXE) list >> $(DEBUG_FILE)

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help


print-%  : ; @echo $* = $($*)

HELP_VARS := PROJECT_NAME DEBUG_FILE

help-prefix:
	@echo "To get started:"
	@echo "  >>> $$(tput bold)make create_environment$$(tput sgr0)"
	@echo "  >>> $$(tput bold)conda activate $(PROJECT_NAME)$$(tput sgr0)"
	@echo ""
	@echo "$$(tput bold)Project Variables:$$(tput sgr0)"
	@echo ""

show-help: help-prefix $(addprefix print-, $(HELP_VARS))
	@echo
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
