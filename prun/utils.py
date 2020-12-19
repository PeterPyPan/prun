import shutil
import os
from pathlib import Path
import re
import sys

from ._constants import _ENVIRON_VENV_DIR, _DEFAULT_VENV_DIR
from ._constants import _PYTHON_EXEC
from ._constants import _THIS_PLATFORM_DEFS, _PLATFORM_DEFS


def get_venv_dir(venv_dir):
    """
    Get the name of the venv dir.

    If a name is provided, the name will be returned. If None is provided and a
    environment variable is present with the name `PRUN_ENV_DIR`, the value of the
    environment value will be used. If None is provided and no environment variable is
    present, the default value will be used (`.venv`).

    Args:
        venv_dir (str or None): Name of the venv dir or None for using environment
            variable or default value.

    Returns:
        str: The name of the venv dir.
    """
    # If venv_dir is specified, return it.
    if venv_dir is not None:
        return venv_dir

    # Try to get the venv_dir from the environment variables
    venv_dir = os.environ.get(_ENVIRON_VENV_DIR)

    # If venv_dir is specified, return it.
    if venv_dir is not None:
        return venv_dir

    # Fall back to the default venv_dir.
    return _DEFAULT_VENV_DIR


def get_executable_in_venv(venv_path, executable, only_scripts=True):
    """
    Get the path to an executable in a virtual environment.

    Args:
        venv_path (str): Full path to an virtual environment folder.

        executable (str): The executable name.

        only_scripts (bool): Whether to look only in the `evn_path/Scripts` (win) or
            `env_path/bin` (linux, osx) folder or to also look in the `env_path` for
            the executable.

    Returns:
        str: The full path to the executable.

    Raises:
        FileNotFoundError: If the executable could not be found in the environment.
    """
    # The folder containing the executables of the environment.
    env_exec_path = os.path.join(venv_path, _THIS_PLATFORM_DEFS['executables_dir'])

    if not only_scripts:
        # Also search in the venv_path folder.
        env_exec_path += os.pathsep + venv_path

    # Find the executable in the path.
    venv_executable = shutil.which(executable, path=env_exec_path)
    if not venv_executable:
        raise FileNotFoundError(
            f'The executable ({executable}) could not be found in {env_exec_path}'
        )

    return venv_executable


def search_python_in_folder_structure(folder, max_search_depth=100):
    """
    Search a folder structure for a virtual environment python executable.

    This function starts deep and moves up in the folder structure to try and find a
    python executable in a virtual environment.

    Args:
        folder (str): The folder to start the search in.
        max_search_depth (int): Maximum upward search depth.

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    # Get the name of the venv dir from the environment variable or fall back to the
    # default value.
    venv_dir = os.environ.get(_ENVIRON_VENV_DIR, _DEFAULT_VENV_DIR)

    folder_name = None
    for _ in range(max_search_depth):
        if folder_name == '':
            break

        python_exec, venv_exec_path = find_virtual_environment(
            folder=folder, venv_dir=venv_dir
        )
        if python_exec is not None:
            return python_exec, venv_exec_path

        folder, folder_name = os.path.split(folder)
    return None, None


def find_virtual_environment(folder, venv_dir):
    """
    Search a single folder for a virtual environment python executable.

    Args:
        folder (str): Folder to find the virtual environment python executable in.
        venv_dir (str): Virtual environment folder name.

    Returns:
        str or None: Path to the python executable or None if it was not found.
    """
    # The name of the executables folder of a virtual environment.
    exec_dir_name = _THIS_PLATFORM_DEFS['executables_dir']

    # Define search path.
    venv_path = os.path.join(folder, venv_dir)
    venv_exec_path = os.path.join(venv_path, exec_dir_name)
    venv_search_path = os.pathsep.join((venv_exec_path, venv_path))

    # Find the executable. This will return None if not found.
    python_exec = shutil.which(_PYTHON_EXEC, path=venv_search_path)

    return python_exec, venv_exec_path


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
