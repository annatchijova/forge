import json


def save(conn, contradictions, confidence_warnings):
    # One column value in a parameterized SQL row - the row itself already
    # carries its own version column (cronos_version), not a standalone
    # JSON document.
    conn.execute(
        "INSERT INTO traces (contradictions, confidence_warnings, cronos_version) VALUES (?, ?, ?)",
        (
            json.dumps(contradictions or []),
            json.dumps(confidence_warnings or []),
            1,
        ),
    )
