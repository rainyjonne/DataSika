# How to set up [pyenv](https://github.com/pyenv/pyenv)?

## [Install pyenv](https://github.com/pyenv/pyenv#installation)
  - macOS:
        1. `brew update`
        2. `brew install pyenv`
  - WSL2, Linux:
        1. `sudo apt-get update; sudo apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`
        2. `git clone https://github.com/pyenv/pyenv.git ~/.pyenv`

## [Pyenv Shell Environment Set Up](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)
  - Execute these lines into your `~/.bashrc` or `~/.zshrc` (You can use `echo $SHELL` to see you are `bash` or `zsh` shell
    - for `~/.bashrc`
        ```
        echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        ```
    - for `~/.zshrc`
        ```
        echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        ```
  - Execute these lines into your `~/.profile` or `~/.zprofile`
    - for `~/.profile`
        ```
        echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.profile
        echo 'eval "$(pyenv init --path)"' >> ~/.profile.
        ```
    - for `~/.zshrc`
        ```
        echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.zprofile
        echo 'eval "$(pyenv init --path)"' >> ~/.zprofile.
        ```
  - if it doesn't work, see the link above to dig out more information

## (Optional) [Install pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
  - macOS:
        1. `brew install pyenv-virtualenv`
        2. Put this line into your `~/.bashrc` or `~/.zshrc`: `echo 'eval "$(pyenv virtualenv-init -)"'`
        3. Remember to restart your shell by `exec "$SHELL"` in your terminal
  - WSL2, Linux:
        1. `git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv`
        2. Put this line into your `~/.bashrc` or `~/.zshrc`: `echo 'eval "$(pyenv virtualenv-init -)"'`
        3. Remember to restart your shell by `exec "$SHELL"` in your terminal

## (Optional) Create an virtualenvironment for yourself
  - Execute this command in your terminal: `pyenv virtualenv 3.x.x <your-virtual-env-name>`, replace the python version with the one you just installed and give a name for your virtual environment
  - Activate your environment: `pyenv activate <your-virtual-env-name>`
  - Put `<your-virtual-env-name>` in to the `.python-version` file's first line, the environment will automatically change your environment to this virtual environment you just made, you can do it by execute this command: `echo <your-virtual-env-name> >> .python-version`.
  - (Optional) If you want to deactivate your environment: `pyenv deactive <your-virtual-env-name>`

## Shell Environment Set Up
  - Use Pyenv to install python versions
    - This project support 3 python versions (3.7.13, 3.8.13, 3.9.11), you can choose one to install.
    - Execute this command in terminal: `pyenv install 3.x.x`
    - Set this python version as your default python version: `pyenv global 3.x.x`
    - Change the `.python-version` file in the project root, add in the python version on the first line in the `.python-version` file: `3.x.x`, you can do it by execute this command: `echo 3.x.x >> .python-version`.
    - Your project environment would be set to that version of python automatically.
