import subprocess


def render(command):
    return subprocess.run(command, shell=True)
