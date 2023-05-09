import os

def error(message: str):
    print(f"ERROR: {message}")
    os._exit(1)