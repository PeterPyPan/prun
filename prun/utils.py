from distutils.spawn import find_executable
import os

from ._constants import _ENVIRON_VENV_DIR, _DEFAULT_VENV_DIR
from ._constants import _PYTHON_EXEC
from ._constants import _THIS_PLATFORM_DEFS


def get_venv_dir():
    """
    Get the name of the venv dir.

    If an environment variable is present with the name `PVENV_ENV_DIR`, the value of
    the environment value will be returned. Otherwise, the default value will be used
    (`.venv`).

    Returns:
        str: The name of the venv dir.
    """
    # Try to get the venv_dir from the environment variables
    venv_dir = os.environ.get(_ENVIRON_VENV_DIR, _DEFAULT_VENV_DIR)

    # If venv_dir is specified, return it.
    if venv_dir is not None:
        return venv_dir

    # Fall back to the default venv_dir.
    return _DEFAULT_VENV_DIR


def search_python_in_folder_structure(folder, max_search_depth=100):
    """
    Search a folder structure for a virtual environment python executable.

    This function starts deep and moves up in the folder structure to try and find a
    python executable in a virtural environment.

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
    python_exec = find_executable(executable=_PYTHON_EXEC, path=venv_search_path)

    return python_exec, venv_exec_path
