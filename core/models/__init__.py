#!/usr/bin/env python3

from importlib import import_module
from os.path import abspath
from pathlib import Path

THIS_FILE = Path(abspath(__file__))
THIS_FOLDER = THIS_FILE.parent
MODULE_NAMES = [
    file.name[:file.name.index(".")] for file in THIS_FOLDER.glob("*.py")
        if file.name[0] != "_"
]
for name in MODULE_NAMES:
    import_module(f'.{name}', THIS_FOLDER.name)
    inner_class = (
        vars(
            globals().get(name)
        ).get(
            name.capitalize()
        )
    )
    globals()[name.capitalize()] = inner_class
    del name, inner_class

__all__ = [name.capitalize() for name in MODULE_NAMES]
