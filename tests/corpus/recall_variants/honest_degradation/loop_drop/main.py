def build_signals(raw_items):
    signals = []
    for item in raw_items:
        try:
            signals.append(Signal(item["tool"], item["value"]))
        except Exception:
            logger.error("invalid signal ignored")
            continue
    return signals
