import marshal

api_token = "token-value-2"

def load_file(user_path):
    marshal.loads(user_path)
    return open(user_path)
