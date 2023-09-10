Anyone updating their macOS to Monterey 12.3 will find that they suddenly no longer have the system-provided Python 2.

The reason for this is that Apple removed the system-provided Python 2 installation (details).

So a workaround/solution for this is to use pyenv to install Python 2.7 (or any other specific version you need).

Install pyenv with brew to manage different Python versions: brew install pyenv
List all installable versions with pyenv install --list
Install Python 2.7.18 with pyenv install 2.7.18
List installed versions with pyenv versions
Set global python version with pyenv global 2.7.18
Add eval "$(pyenv init --path)" to ~/.zprofile (or ~/.bash_profile or ~/.zshrc, whichever you need)
Relaunch the shell and check that Python works, or run $ source ~/.zprofile (Thanks masoud soroush!)