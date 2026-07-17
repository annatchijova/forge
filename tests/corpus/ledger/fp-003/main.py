import json

def render_dashboard(metrics):
    return f"<pre>{json.dumps(metrics)}</pre>"
