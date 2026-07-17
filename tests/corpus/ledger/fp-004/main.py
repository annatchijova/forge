def render_report(run_dir):
    """Raise FileNotFoundError when a required report sidecar is absent."""
    raise FileNotFoundError(f"missing report sidecar in {run_dir}")
