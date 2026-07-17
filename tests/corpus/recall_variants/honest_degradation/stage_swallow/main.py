def analyze(signal):
    try:
        caie = run_caie(signal.metadata)
    except Exception:
        logger.warning("CAIE failed non-blocking")
        caie = None
    return build_result(signal, caie)
