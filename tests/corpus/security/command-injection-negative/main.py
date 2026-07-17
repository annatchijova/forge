import subprocess

def version():
    return subprocess.run(["convert", "--version"], check=True)
