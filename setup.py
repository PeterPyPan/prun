from setuptools import setup, find_packages

package_name = 'prun'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name=package_name,
      version='0.0.1',
      description='A convenience app for working with virtual environments like a breeze.',
      author='PeterPyPan',
      author_email='PeterPyPanGitHub@gmail.com',
      packages=find_packages('.'),
      package_data={},
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PeterPyPan/prun',
      python_requires='>=3',
      install_requires=[],
      extras_require={},
      entry_points={'console_scripts': ['prun=prun:main']},
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      keywords='virtual environment venv virtualenv pipenv',
      )
