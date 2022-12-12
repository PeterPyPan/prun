from argparse import ArgumentParser
import logging
import os
import subprocess
import sys
import shutil

from .utils import get_venv_dir, get_executable_in_venv
from ._constants import _PYTHON_EXEC
from ._constants import _PRE_COMMIT_EXEC
from ._constants import _PRE_COMMIT_CONFIG
from ._constants import _REQUIREMENTS_NAME
from ._constants import _CONDA_ENVIRONMENT_NAME
from ._constants import _CONDA_EXEC


logging.basicConfig(format='PVENV:%(levelname)s:%(message)s', level=logging.DEBUG)


def ensure_venv(project_dir, venv_dir):
    """
    Ensure that a virtual environment exists.

    Create a new venv named `venv_dir` in the `project_dir` if it does not exist yet.
    If a venv already exists, make sure it is valid.

    Args:
        project_dir (str): The project folder.
        venv_dir (str): The folder name of the virtual environment.

    Returns:
        str: The full path to the virtual environment folder.

    Raises:
        FileNotFoundError: When a virtual environment folder exists, but it does not
            contain a Python executable in the expected location.
    """
    # Define the full path to the virtual environment.
    venv_path = os.path.join(project_dir, venv_dir)

    # If the venv does not exist, create it.
    if not os.path.exists(venv_path):
        subprocess.check_call(
            [sys.executable, '-m', 'venv', venv_path], cwd=project_dir
        )
        return venv_path

    # If the venv exists, check that it contains a python executable.
    try:
        get_executable_in_venv(venv_path=venv_path, executable=_PYTHON_EXEC)
    except FileNotFoundError:
        raise FileNotFoundError(
            f'The existing virtual environment seems to be broken: {venv_path}.'
        )

    return venv_path


def resolve_project_dir(project_dir):
    """
    Resolve the project dir to an absolute path.

    Args:
        project_dir (str or None): Path to the project folder. If None, the project
            folder will be the current working directory.

    str: The absolute path to the project folder.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    project_dir = os.path.abspath(project_dir)
    if not os.path.isdir(project_dir):
        raise NotADirectoryError(
            f'The project directory could not be resolved: {project_dir}.'
        )
    return project_dir


def setup_venv(project_dir, venv_dir, requirements_path, clear=False):
    """
    Setup a virtual environment in the project folder.

    As a first step, a virtual environment will be ensured. Next, pip will be upgraded
    to the latest version. Finally the requirements of the `requirments.txt` file will
    be installed.

    Args:
        project_dir (str or None): Path to the project folder. If None, the project
            folder will be the current working directory.

        venv_dir (str): The folder name of the virtual environment.

        requirements_path (str): The path to the requirements file.

        clear (bool): Whether to clear the virtual environment before installing the
            requirements. Currently `clear=True` is not implemented.

    Returns:
        str: The full path to the virtual environment.
    """
    if clear:
        raise NotImplementedError(
            'Clearing is not implemented yet for a standard venv.'
        )

    # Ensure the venv exists.
    logging.info('Ensuring venv...')
    venv_path = ensure_venv(project_dir=project_dir, venv_dir=venv_dir)
    logging.info('Ensuring venv done.')

    # Get python executable.
    venv_python = get_executable_in_venv(venv_path=venv_path, executable=_PYTHON_EXEC)

    # Upgrade pip.
    logging.info('Upgrading pip...')
    subprocess.run(
        [
            venv_python,
            '-m',
            'pip',
            'install',
            '--upgrade',
            'pip',
        ],
        cwd=project_dir,
        check=True,
    )
    logging.info('Upgrading pip done.')

    # Install core pip packages.
    logging.info('Installing core pip packages...')
    subprocess.run(
        [
            venv_python,
            '-m',
            'pip',
            'install',
            '--upgrade',
            'wheel',
        ],
        cwd=project_dir,
        check=True,
    )
    logging.info('Installing core pip packages done.')

    # Install requirements.
    logging.info('Installing requirements...')
    subprocess.run(
        [venv_python, '-m', 'pip', 'install', '-r', requirements_path],
        cwd=project_dir,
        check=True,
    )
    logging.info('Installing requirements done.')

    return venv_path


def setup_conda_env(project_dir, venv_dir, conda_environment_path, clear=False):
    """
    Setup a conda environment.

    Args:
        project_dir (str or None): Path to the project folder. If None, the project
            folder will be the current working directory.

        venv_dir (str): The folder name of the environment.

        conda_environment_path: The path to the `environment.yml` file.

        clear (bool): Whether to prune the Conda environment and make sure the only the
            minimal set of dependencies remains.

    Returns:
        str: The full path to the environment.
    """
    # Get the conda executable.
    conda_executable = shutil.which(_CONDA_EXEC)
    if not conda_executable:
        raise FileNotFoundError(
            f'The {_CONDA_EXEC} executable could not be found. '
            f'To use conda, it must be added to your system path.'
        )

    # Define the
    venv_path = os.path.join(project_dir, venv_dir)

    # Decide if we need to create or update the conda environment.
    extra_args = []
    if not os.path.exists(venv_path):
        conda_command = 'create'
        log_word = 'Creating'
    else:
        conda_command = 'update'
        log_word = 'Updating'
        if clear:
            extra_args += ['--prune']

    # Create/Update the environment.
    logging.info(f'{log_word} conda env...')
    cmd_args = [
        _CONDA_EXEC,
        'env',
        conda_command,
        '--file',
        conda_environment_path,
        '--prefix',
        venv_path,
    ]
    cmd_args += extra_args
    subprocess.check_call(cmd_args, cwd=project_dir, shell=True)
    logging.info(f'{log_word} conda env done.')

    return venv_path


def install_pre_commit_hooks(project_dir, env_path):
    """
    Install the pre-commit hooks for a project if necessary.

    Args:
        project_dir (str): The path to the project folder.
        env_path (str): The full path to the environment.
    """
    # Check if the pre-commit config file is present.
    pre_commit_config_file = os.path.join(project_dir, _PRE_COMMIT_CONFIG)
    if not os.path.exists(pre_commit_config_file):
        logging.info('Skip installing pre-commit hooks.')
        return

    # Get the pre-commit executable.
    try:
        pre_commit_exec = get_executable_in_venv(
            venv_path=env_path, executable=_PRE_COMMIT_EXEC
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            'The pre-commit executable could not be found in your venv.\n'
            'Make sure that you added a `pre-commit` requirement to your requirements '
            'file.'
        )

    # Run pre-commit install.
    logging.info('Installing pre-commit hooks...')
    subprocess.run(
        [
            pre_commit_exec,
            'install',
        ],
        cwd=project_dir,
        check=True,
    )
    logging.info('Installing pre-commit hooks done.')


def setup_environment(venv_dir=None, project_dir=None, clear=False):
    """

    Args:
        venv_dir:
        project_dir:
        clear:

    Returns:

    """
    # Get project and venv dir.
    project_dir = resolve_project_dir(project_dir=project_dir)
    venv_dir = get_venv_dir(venv_dir=venv_dir)

    # Figure out if we are dealing with a conda environment or virtual environment.
    requirements_path = os.path.join(project_dir, _REQUIREMENTS_NAME)
    conda_environment_path = os.path.join(project_dir, _CONDA_ENVIRONMENT_NAME)
    if os.path.exists(conda_environment_path):
        logging.info(
            f'Detected conda {_CONDA_ENVIRONMENT_NAME} file, assuming conda project.'
        )
        env_path = setup_conda_env(
            project_dir=project_dir,
            venv_dir=venv_dir,
            conda_environment_path=conda_environment_path,
            clear=clear,
        )
    elif os.path.exists(requirements_path):
        logging.info(
            f'Detected pip {_REQUIREMENTS_NAME} file, assuming standard venv project.'
        )
        env_path = setup_venv(
            project_dir=project_dir,
            venv_dir=venv_dir,
            requirements_path=requirements_path,
            clear=clear,
        )
    else:
        raise FileNotFoundError(
            f'Cannot setup an environment without a `{_REQUIREMENTS_NAME}` or '
            f'`{_CONDA_ENVIRONMENT_NAME}` file in the project folder: {project_dir}.'
        )

    # Install pre-commit hooks if necessary.
    install_pre_commit_hooks(project_dir=project_dir, env_path=env_path)


def parse_args():
    parser = ArgumentParser(
        description='Setup a virtual environment or a conda environment for a project.'
        f'If a `{_CONDA_ENVIRONMENT_NAME}` file is present, a conda '
        f'environment will be set up. If a `{_REQUIREMENTS_NAME}` file is '
        f'present, a normal virtual environment will be created.'
    )

    parser.add_argument(
        '--venv-dir',
        default=None,
        help=f'Name of the virtual environment directory.',
    )

    parser.add_argument(
        '--project-dir',
        default=None,
        help='Normally you run `pvenv` in your main project folder. '
        'If you want to setup a virtual environment from outside of your project '
        'folder, you can specify its path with this parameter.',
    )

    parser.add_argument(
        '--clear',
        '-c',
        default=False,
        action='store_true',
        help='Adding this flag will ensure that the virtual environment will have only'
        f'the requirements from the `{_CONDA_ENVIRONMENT_NAME}` or '
        f'`{_REQUIREMENTS_NAME}` file.',
    )

    # Return the arguments as a dict.
    args = parser.parse_args()
    return {
        'venv_dir': args.venv_dir,
        'project_dir': args.project_dir,
        'clear': args.clear,
    }


def main():
    """Main function for `pvenv`."""
    try:
        kwargs = parse_args()
        setup_environment(**kwargs)
    except Exception:
        logging.exception('`pvenv` has encountered a fatal error.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    main()
