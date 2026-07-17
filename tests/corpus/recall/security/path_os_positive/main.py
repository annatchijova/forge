import os


@app.post("/download")
def artifact_path(user_path):
    return os.path.join("/srv/artifacts", user_path)
