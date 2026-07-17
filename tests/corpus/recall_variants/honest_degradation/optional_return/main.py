def get_nickname(data):
    try:
        return data["nickname"]
    except KeyError:
        return None
