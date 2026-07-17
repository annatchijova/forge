class Engine:
    def to_signal(self, raw):
        try:
            return convert(raw)
        except Exception as exc:
            self._signal_drops.append(str(exc))
            return self._unanalyzed_signal("engine", str(exc))
