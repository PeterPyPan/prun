import os
import sys
import subprocess
import shutil
from pathlib import Path
import re

from ._constants import (
    _THIS_PLATFORM_DEFS,
    _PLATFORM_DEFS,
    _PYTHON_EXEC,
    _CONDA_META_FOLDER,
    _ACTIVATE_EXEC,
    _CONDA_EXEC,
)
from .utils import search_python_in_folder_structure


def platformed_path(path, platform, add_quotes=True):
    # Remove quotes and convert to path.
    path = Path(path.strip('"').strip("'"))

    # Convert path to target platform definition.
    if platform != sys.platform:
        path_class = _PLATFORM_DEFS[platform]['path_class']
        path = path_class(path)

    # Convert back to string.
    path = str(path)

    # Windows to posix conversion for drives.
    if sys.platform == 'win32' and platform != 'win32':
        # Try to find drive letters in the path
        m = re.match('^([A-Za-z]):\\\\', path)

        # Resolve drive letters if necessary.
        if m is not None:
            path = f'{m.group(1)}:{path[m.span()[1]:]}'

    elif sys.platform != 'win32' and platform == 'win32':
        raise NotImplementedError('Conversion from posix to win32 not implemented.')

    if add_quotes:
        quote_char = _PLATFORM_DEFS[platform]['path_quote']
        path = f'{quote_char}{path}{quote_char}'

    return path


def main():
    # Get the current working directory.
    current_dir = os.getcwd()

    # Search the python executable folder in the current working directory.
    python_exec, exec_path = search_python_in_folder_structure(folder=current_dir)
    if python_exec is None:
        raise ValueError('No virtual environment was found.')
    venv_path = os.path.abspath(os.path.join(exec_path, '..'))

    # Add the venv executables folder to the path environment variable.
    env = os.environ.copy()
    env['PATH'] = os.pathsep.join(filter(None, [exec_path, os.environ.get('PATH', '')]))

    # Process the command line arguments for special tasks.
    cli_args = sys.argv[1:]
    cli_args_proc, force_platform = process_cli_args(
        cli_args=cli_args, env_path=env['PATH']
    )
    # Make sure platform is specified.
    if force_platform is None:
        force_platform = sys.platform
    if cli_args_proc[0] is None:
        print(_THIS_PLATFORM_DEFS['msg_not_found'] % cli_args[0])
        sys.exit(1)

    # Special `prun activate` case. Supports both standard venv and conda envs.
    if cli_args_proc[0] == _ACTIVATE_EXEC:
        prun_activate(
            venv_path=venv_path, exec_path=exec_path, force_platform=force_platform
        )
        return

    # Run the command.
    try:
        subprocess.run(cli_args_proc, universal_newlines=True, env=env, check=True)
    except FileNotFoundError:
        print(_THIS_PLATFORM_DEFS['msg_not_found'] % cli_args_proc[0])
        sys.exit(1)


def prun_activate(venv_path, exec_path, force_platform):
    conda_meta_folder = os.path.join(venv_path, _CONDA_META_FOLDER)
    if os.path.exists(conda_meta_folder):
        # Conda environment.
        conda_exec = shutil.which(_CONDA_EXEC)
        if conda_exec is None:
            print(_THIS_PLATFORM_DEFS['msg_not_found'] % conda_exec)
            sys.exit(1)
        cmd_args = [
            _CONDA_EXEC,
            _ACTIVATE_EXEC,
            platformed_path(venv_path, platform=force_platform),
        ]

    else:
        # Normal venv.
        activate_exec = shutil.which(_ACTIVATE_EXEC, path=exec_path)
        if activate_exec is None:
            print(_THIS_PLATFORM_DEFS['msg_not_found'] % activate_exec)
            sys.exit(1)
        # Revert back to activate without an extension.
        activate_exec = os.path.join(exec_path, _ACTIVATE_EXEC)
        activate_exec = platformed_path(activate_exec, platform=force_platform)
        cmd_args = _PLATFORM_DEFS[force_platform]['activate_prefix'] + [activate_exec]

    # Print the activate command.
    print(' '.join(cmd_args), end='')


def process_cli_args(cli_args, env_path):
    """
    Process the list of command line arguments.

    Args:
        cli_args (list of str): list of command line arguments
        env_path (str): path for finding executables to construct cli args

    Returns:
        list of str: processed list of command line arguments
    """
    # Deep copy the input arguments.
    cli_args = list(cli_args)

    # Initialize force_platform.
    force_platform = None

    if len(cli_args) == 0:
        # If no cli args, add python.
        cli_args = [_PYTHON_EXEC]

    if cli_args[0].endswith('.py'):
        # If first argument is a python file, add python.
        cli_args = [_PYTHON_EXEC] + cli_args

    if cli_args[0] == '-show':
        # If first argument is -show, show the path to the found python.
        cli_args = [_THIS_PLATFORM_DEFS['-show'], _PYTHON_EXEC]
    elif cli_args[0] == '-h' or cli_args[0] == '-help':
        print(
            'prun help: \n'
            '  Running a command using the local virtual environment:\n'
            '    prun command arg1 arg2 ...\n'
            '  Running python from the local virtual environment:\n'
            '    prun\n'
            '  Running a python file from the local virtual environment:\n'
            '    prun script.py arg1 arg2\n'
            '  Show the path to the python executable of the virtual environment:\n'
            '    prun -show\n'
            '  Return a string that can be used to activate the virtual environment:\n'
            '  To activate in linux use `source $(prun activate)`.\n'
            '  To activate in windows use ``'
            '    prun activate\n'
            '  Show the prun help\n'
            '    prun -h'
        )
        sys.exit(0)
    else:
        # cli_args[0] is an executable.
        if cli_args[0] == _ACTIVATE_EXEC:
            # Activate executable
            if len(cli_args) == 2:
                if cli_args[1] not in _PLATFORM_DEFS.keys():
                    raise ValueError(
                        f'The provided platform ({cli_args[1]}) is invalid.'
                        f'Possible values are: {list(_PLATFORM_DEFS.keys())}'
                    )
                force_platform = cli_args[1]

            if len(cli_args) > 2:
                raise ValueError(
                    'When using prun activate, it is not possible to provide '
                    'additional parameters.'
                )
        else:
            # All other executables.
            cli_args[0] = shutil.which(cli_args[0], path=env_path)

    return cli_args, force_platform


if __name__ == '__main__':
    main()
