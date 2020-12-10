from importlib.metadata import version
from . import store
from . import schemas

from .tools import (
    connect_and_initialize,
    get_or_create_seldon_artifact_types,
    save_seldon_model_to_store,
    load_seldon_models_from_store,
)


__all__ = [
    "schemas",
    "store",
    "get_or_create_seldon_artifact_types",
    "save_seldon_model_to_store",
    "load_seldon_models_from_store",
    "connect_and_initialize",
]


try:
    # This will read version from pyproject.toml
    __version__ = version(__name__)
except Exception:
    __version__ = "unknown"
    pass
