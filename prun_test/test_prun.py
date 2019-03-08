import os
import shutil
from prun import find_virtual_environment, process_cli_args
from prun import search_python_in_folder_structure, _get_system_specific_vars


_prun_test_folder = os.path.dirname(os.path.abspath(__file__))
_mockup_folder = os.path.join(_prun_test_folder, '..', 'prun_test_mockup')
_side_folder_list = ['a', 'b', 'c', 'd']


def clean_mockup_folder(folder):
    try:
        shutil.rmtree(folder)
    except FileNotFoundError:
        pass


def create_mockup_sidefolder(folder, folder_list):
    folder_structure = [folder] + folder_list
    new_folder = os.path.join(*folder_structure)
    os.makedirs(new_folder, exist_ok=True)
    return new_folder


def create_mockup_venv(folder, venv_folder, win32=True):
    # cleanup previous mockup folders
    clean_mockup_folder(folder)

    # create fake virtual environement folder structure
    exec_folder_name = 'bin'
    if win32:
        exec_folder_name = 'Scripts'
    exec_folder = os.path.join(folder, venv_folder, exec_folder_name)
    os.makedirs(exec_folder, exist_ok=True)

    # create fake python executable
    exec_name = 'python'
    if win32:
        exec_name = 'python.exe'
    exec_path = os.path.join(exec_folder, exec_name)
    with open(exec_path, 'w'):
        pass

    return exec_path


def test_process_cli_args():
    args = []
    p_args = process_cli_args(cli_args=args)
    assert p_args == ['python']

    args = ['myscript.py']
    p_args = process_cli_args(cli_args=args)
    assert p_args == ['python'] + args

    args = ['myscript.py', '10', '-verbose']
    p_args = process_cli_args(cli_args=args)
    assert p_args == ['python'] + args

    args = ['-show']
    p_args = process_cli_args(cli_args=args)
    assert p_args == ['which', 'python']

    args = ['test', 'all', '-the', 'things', '10']
    p_args = process_cli_args(cli_args=args)
    assert p_args == args


def test_find_virtual_environment_win32():
    # win32
    _, exec_folder, exec_name = _get_system_specific_vars('win32')

    venv_folder = '.venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=True)
    python_exec = find_virtual_environment(_mockup_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    venv_folder = 'venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=True)
    python_exec = find_virtual_environment(_mockup_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    # cleanup the mockup folder
    clean_mockup_folder(_mockup_folder)


def test_find_virtual_environment_darwin():
    # osx
    _, exec_folder, exec_name = _get_system_specific_vars('darwin')

    venv_folder = '.venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=False)
    python_exec = find_virtual_environment(_mockup_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    venv_folder = 'venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=False)
    python_exec = find_virtual_environment(_mockup_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    # cleanup the mockup folder
    clean_mockup_folder(_mockup_folder)


def test_search_python_in_folder_structure_win32():
    # win32
    _, exec_folder, exec_name = _get_system_specific_vars('win32')

    venv_folder = '.venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=True)
    side_folder = create_mockup_sidefolder(_mockup_folder, _side_folder_list)
    python_exec = search_python_in_folder_structure(side_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    venv_folder = 'venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=True)
    side_folder = create_mockup_sidefolder(_mockup_folder, _side_folder_list)
    python_exec = search_python_in_folder_structure(side_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    # cleanup the mockup folder
    clean_mockup_folder(_mockup_folder)


def test_search_python_in_folder_structure_win32():
    # win32
    _, exec_folder, exec_name = _get_system_specific_vars('darwin')

    venv_folder = '.venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=False)
    side_folder = create_mockup_sidefolder(_mockup_folder, _side_folder_list)
    python_exec = search_python_in_folder_structure(side_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    venv_folder = 'venv'
    mockup_exec = create_mockup_venv(_mockup_folder, venv_folder, win32=False)
    side_folder = create_mockup_sidefolder(_mockup_folder, _side_folder_list)
    python_exec = search_python_in_folder_structure(side_folder, exec_folder, exec_name)
    assert os.path.abspath(python_exec) == os.path.abspath(mockup_exec)

    # cleanup the mockup folder
    clean_mockup_folder(_mockup_folder)
