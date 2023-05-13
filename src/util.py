import os, pathlib

# TODO: maybe have some kind of config?
#      or use defaults.json to let users
#      choose out directory?
OUT_DIRECTORY = pathlib.Path("./out")
DEFAULTS_PATH = pathlib.Path("./defaults.json")


def error(message: str):
    print(f"ERROR: {message}")
    os._exit(1)

DEBUG = True
def debug(message: str):
    """
    DEBUG
    """
    if DEBUG:
        print(f"DEBUG: {message}")