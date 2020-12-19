# Conda project with a Python library
This example shows a Conda project setup that includes a Python library (`mylib`). The 
dependencies of the library are defined in the `setup.py` file. Make sure to add an 
editable installation of the library to the `environment.yml` file. Development 
dependencies are defined in the `environment.yml` file.

- Use `pvenv` to setup the Conda environment. 
- Use `prun` to run scripts using the Conda environment.
- Use `pactivate` to activate the Conda environment.

```
# Go into the project folder.
cd examples/venv_with_lib

# Run pvenv to setup the conda environment based 
# on the `environment.yml` file.
pvenv

# Run `my_script.py` without activating.
prun my_script.py
# Prints:
# What a nice array: [1. 2. 3.]

# Activate the virtual environment.
pactivate

# List installed Conda packages (after activating).
conda list

# Deactivate the virtual environment.
conda deactivate
```
