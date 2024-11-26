.PHONY: tests

# useful for debugging
default:
	echo @ makefile

## builds the virtual environment and attaches it to the ipykernel to be used
build_venv:
	pip install --upgrade pip;
	python3.11 -m venv .venv;
	source .venv/bin/activate && pip install -r requirements.txt;
	source .venv/bin/activate && pip install ipykernel
	source .venv/bin/activate && python3.11 -m ipykernel install --user --name=.venv;

# source env/bin/activate; pytest -vvx tests/  # boto is being weird
## runs the package tests
tests: update # only non integration tests
	source env/bin/activate; pytest tests -vvx -p no:warnings

## updates the astronomy ai github
update_Astronomy_AI:
	cd AI-for-Astronomy && git pull

## install the prediction function to be used elsewhere
install_package:
	pip install -e .

# only useful for markdown readme
generate_file_structure:
	tree -L 1

## runs Google Style Guide Linter
lint:
	pylint /src

## runs black to auto format code
format:
	black /src

## clean up the repo
clean:
	echo "add what files to clean up"


.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
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