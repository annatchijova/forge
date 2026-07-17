def to_signal(raw):
    try:
        return Signal(raw["tool"], raw["value"])
    except Exception:
        logger.warning("signal conversion failed")
        return None
