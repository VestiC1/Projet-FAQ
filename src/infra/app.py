import modal

app = modal.App("retrieval-service")

# These imports register the functions/classes on the app
from . import embedding  # noqa: F401, E402
from . import retrieval  # noqa: F401, E402