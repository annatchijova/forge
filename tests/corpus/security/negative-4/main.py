import os

# No default: nothing to leak if unset.
NO_DEFAULT_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Placeholder default: not a real credential.
PLACEHOLDER_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

# Default is not a credential-shaped env var name.
REQUEST_TIMEOUT = os.getenv("REQUEST_TIMEOUT", "30")
