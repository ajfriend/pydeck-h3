.PHONY: env lab clean purge kill

env:
	virtualenv -p python3 env
	env/bin/pip install --upgrade pip
	env/bin/pip install -r requirements.txt
	bash -l -c 'nvm install 14; nvm exec 14 env/bin/jupyter labextension install @jupyter-widgets/jupyterlab-manager nbdime-jupyterlab @deck.gl/jupyter-widget@~8.1.*;'

lab:
	bash -l -c 'nvm install 14; nvm exec 14 env/bin/jupyter lab;'

clean:
	find . -type f -name '*.pyc' | xargs rm -r
	find . -type d -name '*.ipynb_checkpoints' | xargs rm -r
	find . -type d -name '*.egg-info' | xargs rm -r
	find . -type d -name '__pycache__' | xargs rm -r
	find . -type d -name '.pytest_cache' | xargs rm -r

purge: clean
	-@rm -rf env


kill:
	# kills the first job in the background
	# use Ctrl-Z to send a job to the background
	# `fg` to bring it back to forecround
	# use `jobs` to see jobs in background
	kill %1
