default:
	echo @ makefile

build_venv:
	pip install --upgrade pip;
	python3.11 -m venv .venv;
	source .venv/bin/activate && pip install -r requirements.txt;
	source .venv/bin/activate && pip install ipykernel
	source .venv/bin/activate && python3.11 -m ipykernel install --user --name=.venv;

.PHONY: tests
tests: update # only non integration tests
	source env/bin/activate; pytest -vvx tests/

update_Astronomy_AI:
	cd AI-for-Astronomy && git pull

install_package:
	pip install -e .

generate_file_structure:
	tree -L 1
