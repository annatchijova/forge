import subprocess


def version():
    try:
        return subprocess.run(["tool", "--version"], check=True)
    except subprocess.SubprocessError as exc:
        raise RuntimeError("tool failed") from exc
