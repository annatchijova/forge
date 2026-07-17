def analyze(signal):
    result_flags = {}
    try:
        caie = run_caie(signal.metadata)
    except Exception as exc:
        caie = None
        result_flags["caie_skipped"] = str(exc)
    return build_result(signal, caie, result_flags)
