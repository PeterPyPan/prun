# Venv Project containing a Python library
This example shows a venv project setup that includes a Python library (`mylib`). The 
dependencies of the library are defined in the `setup.py` file. Make sure to add an 
editable installation of the library to the `requirements.txt` file. Development 
dependencies are defined in the `requirements.txt` file.

This project also includes a `pre-commit` configuration (`.pre-commit-config.yaml`) 
that allows to automatically setup pre-commit hooks. In this case, black formatting is 
enabled.

- Use `pvenv` to setup the virtual environment. 
- Use `prun` to run scripts using the virtual environment.
- Use `pactivate` to activate the virtual environment.

```
# Go into the project folder.
cd examples/venv_with_lib

# Run pvenv to setup the virtual environment based 
# on the `requirements.txt` file. This will also
# setup the pre-commit hooks.
pvenv

# Show that all requirements are installed.
prun pip list

# Run `my_script.py` without activating.
prun my_script.py
# Prints:
# What a nice array: [1. 2. 3.]

# Run the pre-commit hooks on `my_script.py`.
prun pre-commit run --files my_script.py

# Activate the virtual environment.
pactivate

# Deactivate the virtual environment.
deactivate
```
