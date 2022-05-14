# Yaml Pipeline Generator
A simple python package that reads in your yaml syntax file and produce a data pipeline for you.
## Compatibility of python versions
### python versions
- 3.7.13
- 3.8.13
- 3.9.11
## Environment SetUp
### Clone this project
- Using command: `git clone git@github.com:rainyjonne/yaml-pipeline-generator.git`
- Manually download: clicking `Download ZIP file` from the green code button 
### Go into the folder of yaml-pipeline-generator
### [Install python directly](https://www.python.org/downloads/)

### Using [pyenv](https://github.com/pyenv/pyenv)
- [Install pyenv](https://github.com/pyenv/pyenv#installation)
  - macOS: 
	1. `brew update`
	2. `brew install pyenv`
  - WSL2, Linux:
	1. `sudo apt-get update; sudo apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`
	2. `git clone https://github.com/pyenv/pyenv.git ~/.pyenv`

- [Pyenv Shell Environment Set Up](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)
  - Put these lines into your `~/.bashrc` or `~/.zshrc`, `~/.zprofile` 
  ```
  export PATH="~/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  ```
  - Put these lines into your `~/.profile` or `~/.zprofile` 
  ```
  export PATH="~/.pyenv/bin:$PATH"
  eval "$(pyenv init --path)"
  ```
  - if it doesn't work, see the link above to dig out more information

- [Install pyenv-virtualenv & Shell Environment Set Up](https://github.com/pyenv/pyenv-virtualenv)
  - macOS:
	1. `brew install pyenv-virtualenv`
	2. Put this line into your `~/.bashrc` or `~/.zshrc`: `echo 'eval "$(pyenv virtualenv-init -)"'`
	3. Remember to restart your shell by `exec "$SHELL"` in your terminal 
  - WSL2, Linux:
	1. `git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv`
	2. Put this line into your `~/.bashrc` or `~/.zshrc`: `echo 'eval "$(pyenv virtualenv-init -)"'` 
	3. Remember to restart your shell by `exec "$SHELL"` in your terminal 

- Use Pyenv to install python versions
  - This project support 3 python versions (3.7.13, 3.8.13, 3.9.11), you can choose one to install.
  - Execute this command in terminal: `pyenv install 3.x.x`
  - Set this python version as your default python version: `pyenv global 3.x.x`
  - Change the `.python-version` file in the project root, add in the python version on the first line in the `.python-version` file: `3.x.x`.
  - Your project environment would be set to that version of python automatically.

- (Optional) Create an virtualenvironment for yourself
  - Execute this command in your terminal: `pyenv virtualenv 3.x.x <your-virtual-env-name>`, replace the python version with the one you just installed and give a name for your virtual environment
  - Activate your environment: `pyenv activate <your-virtual-env-name`
  - Put `<your-virtual-env-name>` in to the `.python-version` file's first line, the environment will automatically change your environment to this virtual environment you just made. 
  - (Optional) If you want to deactivate your environment: `pyenv deactive <your-virtual-env-name>`
 
## Install require packages
- [Install `pip`](https://pip.pypa.io/en/stable/installation/)
  - macOS: `python -m ensurepip --upgrade`
  - WSL, Linux: `python -m ensurepip --upgrade`

- Install other require packages
  - Execute this command in terminal: `pip install -r requirements.txt`

## Running examples
- Making this package's command line tool works: `python setup.py install`
- Running two examples:
  - Using command line tools:
    1. Airbnb + Crime Data Example: `yml-gen --input examples/airbnb_pipeline.yml`
    2. Ruby Gems RepoMiner Example: `yml-gen --input examples/repominer.yml`
  - Using python scripts:
    1. Airbnb + Crime Data Example: `python yaml_pipeline_generator/main.py --input examples/airbnb_pipeline.yml`
    2. Ruby Gems RepoMiner Example: `python yaml_pipeline_generator/main.py --input examples/repominer.yml`

