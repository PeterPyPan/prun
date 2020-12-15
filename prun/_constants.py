import sys
from pathlib import PurePosixPath, PureWindowsPath

# Platform specific definitions
_PLATFORM_DEFS = {
    'win32': {
        'msg_not_found': (
            "'%s' is not recognized as an internal or external command, "
            'operable program or batch file.'
        ),
        'executables_dir': 'Scripts',
        '-show': 'where',
        'path_class': PureWindowsPath,
        'path_quote': '"',
        'activate_prefix': [],
    },
    'linux': {
        'msg_not_found': '%s: command not found',
        'executables_dir': 'bin',
        '-show': 'which',
        'path_class': PurePosixPath,
        'path_quote': '',
        'activate_prefix': ['source'],
    },
}
_PLATFORM_DEFS['darwin'] = {**_PLATFORM_DEFS['linux']}
_THIS_PLATFORM_DEFS = _PLATFORM_DEFS[sys.platform]

# Environment variable name to specify default folder name for virtual environment.
_ENVIRON_VENV_DIR = 'PVENV_ENV_DIR'

# Default folder name for the virtual environment.
_DEFAULT_VENV_DIR = '.venv'

# Python executable.
_PYTHON_EXEC = 'python'

# Conda executable.
_CONDA_EXEC = 'conda'

# Activate executable.
_ACTIVATE_EXEC = 'activate'

# Conda meta folder.
_CONDA_META_FOLDER = 'conda-meta'
