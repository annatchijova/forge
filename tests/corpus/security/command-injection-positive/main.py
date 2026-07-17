import subprocess

@app.post("/convert")
def convert(name):
    return subprocess.run(["convert", f"--name={name}"], check=True)
