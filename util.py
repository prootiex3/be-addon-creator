import os, pathlib

OUT_DIRECTORY = pathlib.Path("./out")


def error(message: str):
    print(f"ERROR: {message}")
    os._exit(1)
