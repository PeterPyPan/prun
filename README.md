# prun readme
`prun` is a convenience package for working with virtual/conda environments. It 
contains three executables: `pvenv`, `prun` and `pactivate`. The `examples` folder 
contains several example project setups with a readme file, to explain the use of 
`pvenv`, `prun` and `pactivate`. There are examples for conda and virutal environment 
projects.

- Use `pvenv` to create and manage virtual/conda environments for a project. Based on 
  the presence of a `environment.yml` (conda) or a `requirements.txt` (venv) file, 
  `pvenv` will create a local environment for you.

- Use `prun` within a project folder that contains a virtual/conda environment to 
  automatically work with the python of the virtual/conda environment, without the 
  need of activating the environment.

- Use `pactivate` within a project folder that contains a virtual/conda environment to 
  automatically activate the environment.


## prun installation
`prun` should be installed in your system python and the `<PythonFolder>/Scripts` (win) 
or `<PythonFolder>/bin` folder needs to be added to the path. This makes sure that the 
installed `prun`, `pvenv` and `pactivate` executables can be found.

If you want to use conda environments, you will need to install conda and add the 
`<CondaFolder>/condabin` folder to your path. 

Install `prun` through pip:
```
# Install prun.
python -m pip install prun
# Running this command after installation should let you know that 
# `prun` could not find a virtual environment.
prun -show
# ValueError: No virtual environment was found.
```

## prun settings
`pvenv`, `prun` and `pactivate` assume that your virtual/conda environment folder is 
named `.venv`. If you use a different name for your environments (eg. `venv`), you 
will have to specify an environment value `PVENV_ENV_DIR` (eg `PVENV_ENV_DIR=venv`).
