from setuptools import setup, find_packages

setup(
    name='mylib',
    version='0.0.1',
    packages=find_packages('.'),
    python_requires='>=3',
    install_requires=['numpy'],
)
