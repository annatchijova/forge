def profile(data):
    try:
        nickname = data["nickname"]
    except KeyError:
        nickname = None
    return {"nickname": nickname}
