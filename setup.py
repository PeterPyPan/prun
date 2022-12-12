import glob
import os
from setuptools import setup, find_packages

# Load the readme for the long description.
with open('README.md', 'rt') as fh:
    long_description = fh.read()

# Find the scripts.
_this_path = os.path.realpath(os.path.dirname(__file__))
scripts = glob.glob(os.path.join(_this_path, 'scripts', '*'))

# Call setup.
setup(
    name='prun',
    version='0.4.1',
    description='A convenience app for working with virtual and conda environments.',
    author='PeterPyPan',
    author_email='PeterPyPanGitHub@gmail.com',
    packages=find_packages('.'),
    package_data={},
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PeterPyPan/prun',
    python_requires='>=3',
    install_requires=[],
    entry_points={'console_scripts': ['prun=prun.prun:main', 'pvenv=prun.pvenv:main']},
    scripts=scripts,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='virtual environment venv .venv virtualenv pipenv conda',
)
