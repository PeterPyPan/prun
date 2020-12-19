# Simple venv project
This example shows a simple project setup with a virtual environment. Use the 
`requirements.txt` file to specify your project dependencies. 

- Use `pvenv` to setup the virtual environment. 
- Use `prun` to run scripts using the virtual environment.
- Use `pactivate` to activate the virtual environment.

```
# Go into the project folder.
cd examples/venv_project

# Run pvenv to setup the virtual environment based 
# on the `requirements.txt` file.
pvenv

# Show that all requirements are installed.
prun pip list

# Run `my_script.py` without activating.
prun my_script.py
# Prints:
# What a nice array: [1. 2. 3.]

# Activate the virtual environment.
pactivate

# Deactivate the virtual environment.
deactivate
```
