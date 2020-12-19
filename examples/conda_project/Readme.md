# Simple Conda project
This example shows a simple project setup with a conda environment. Use the 
`environment.yml` file to specify your project dependencies. 

- Use `pvenv` to setup the Conda environment. 
- Use `prun` to run scripts using the Conda environment.
- Use `pactivate` to activate the Conda environment.

```
# Go into the project folder.
cd examples/venv_project

# Run pvenv to setup the conda environment based 
# on the `environment.yml` file.
pvenv

# Run `my_script.py` without activating.
prun my_script.py
# Prints:
# What a nice array: [1. 2. 3.]

# Activate the Conda environment.
pactivate

# List installed Conda packages (after activating).
conda list

# Deactivate the Conda environment
conda deactivate
```
