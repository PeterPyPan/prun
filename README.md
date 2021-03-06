# prun readme

*prun* is a convenience app for working with virtual environments.
Use *prun*  within a folder structure that has a virtual environment folder 
to automatically work with the python of the virtual environment.


First, create a local virtual environment in the *.venv* folder. 
This can be done using the virtualenv package.

```
python -m virtualenv .venv
```


The path to the python executable of the local virtual environment can be printed using the following command:

```
prun -show
```


*prun* can be used to install python packages in the local virtual environment.

```
prun pip install numpy
```


Running a python file, using the python executable from the local virtual environment is easy with *prun*.

```
prun script.py arg0 arg1
```


When executing *prun* without any extra command line arguments, 
the python of the virtual environment will be executed.

```
prun
```

*prun* can run any command line command.

```
prun command arg0 arg1 ...
```
