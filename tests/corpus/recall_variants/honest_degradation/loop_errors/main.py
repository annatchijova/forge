def build_signals(raw_items):
    signals = []
    errors = []
    for item in raw_items:
        try:
            signals.append(Signal(item["tool"], item["value"]))
        except Exception as exc:
            logger.error("invalid signal")
            errors.append((item, exc))
            continue
    return signals, errors
