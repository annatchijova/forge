def build_signals(raw_items):
    signals = []
    for item in raw_items:
        try:
            signals.append(Signal(item["tool"], item["value"]))
        except Exception as exc:
            logger.error("invalid signal")
            signals.append(unanalyzed_marker(item, exc))
    return signals
