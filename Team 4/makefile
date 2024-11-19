default:
	echo @ makefile

# env:
# 	pip install --upgrade pip;
# 	python3.11 -m venv env;
# 	source env/bin/activate && pip install -r requirements.txt;

# install_kernel: env
# 	source env/bin/activate && python3.11 -m ipykernel --user --name env --display-name = "Python (3.11 env)"

build_venv:
	pip install --upgrade pip;
	python3.11 -m venv .venv;
	source .venv/bin/activate && pip install -r requirements.txt;
	source .venv/bin/activate && python3.11 python -m ipykernel install --user --name=CS_Foundations_venv;

.PHONY: tests
tests: update # only non integration tests
	source env/bin/activate; pytest -vvx tests/


can_export_to_pdfs: # note should probably be a script that gets called check for MAC
    conda install nbconvert;
    sudo apt-get update;
    sudo apt-get install pandoc texlive-xetex texlive-fonts-recommended texlive-plain-generic

generate_file_structure:
	tree -L 1

# connect to aws
# check for config file
# 