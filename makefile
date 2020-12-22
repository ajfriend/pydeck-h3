.PHONY: env lab clean purge kill

env:
	python -m venv env
	env/bin/pip install --upgrade pip wheel
	env/bin/pip install -r requirements.txt
	env/bin/pip install -e .
	make test

lab:
	env/bin/jupyter lab

clean:
	find . -type f -name '*.html' | xargs rm -r
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	find . -type d -name '*.egg-info' | xargs rm -r
	find . -type d -name '__pycache__' | xargs rm -r
	find . -type d -name '.pytest_cache' | xargs rm -r
	find . -type f -name '.DS_Store' | xargs rm -r

purge: clean
	-@rm -rf env

test:
	env/bin/pytest
