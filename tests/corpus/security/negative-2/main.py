import os

api_key = os.environ.get("API_KEY")

def read(user_path):
    user_path = os.path.realpath(user_path)
    return open(user_path)
