import os
import pytest
import sys

from prun.pvenv import parse_args, resolve_project_dir

_this_dir = os.path.realpath(os.path.dirname(__file__))


def test_parse_args():
    sys.argv = ['']
    args = parse_args()
    args_exp = {'venv_dir': None, 'project_dir': None, 'clear': False}
    assert args == args_exp

    sys.argv = ['', '--venv-dir', 'venv']
    args = parse_args()
    args_exp = {'venv_dir': 'venv', 'project_dir': None, 'clear': False}
    assert args == args_exp

    sys.argv = ['', '--project-dir', './test/path']
    args = parse_args()
    args_exp = {'venv_dir': None, 'project_dir': './test/path', 'clear': False}
    assert args == args_exp

    sys.argv = ['', '--clear']
    args = parse_args()
    args_exp = {'venv_dir': None, 'project_dir': None, 'clear': True}
    assert args == args_exp

    sys.argv = ['', '-c']
    args = parse_args()
    args_exp = {'venv_dir': None, 'project_dir': None, 'clear': True}
    assert args == args_exp


def test_resolve_project_dir(mocker):
    # project_dir=None
    assert resolve_project_dir(project_dir=None) == os.getcwd()

    # a relative path as a fake project_dir
    rel_path = os.path.join(_this_dir, '..')

    # project_dir=None with patched os.getcwd
    mocker.patch('os.getcwd', return_value=rel_path)
    assert resolve_project_dir(project_dir=None) == os.path.abspath(rel_path)
    mocker.stopall()

    # project_dir=rel_path
    assert resolve_project_dir(project_dir=rel_path) == os.path.abspath(rel_path)

    # project_dir=not_a_dir
    not_a_dir = os.path.join(_this_dir, 'not_a_dir')
    with pytest.raises(NotADirectoryError):
        resolve_project_dir(project_dir=not_a_dir)
