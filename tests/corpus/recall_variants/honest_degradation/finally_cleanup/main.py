def parse_tmp(tmp):
    try:
        return load(tmp)
    finally:
        os.unlink(tmp)
