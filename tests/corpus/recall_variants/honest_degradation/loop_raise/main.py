def build_signals(raw_items):
    signals = []
    for item in raw_items:
        try:
            signals.append(Signal(item["tool"], item["value"]))
        except Exception as exc:
            raise SignalError(item) from exc
    return signals
