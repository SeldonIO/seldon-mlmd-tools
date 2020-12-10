import ml_metadata as mlmd
from ml_metadata.proto import metadata_store_pb2

from . import schemas
from . import store


def connect_and_initialize(address: str = None) -> mlmd.metadata_store.MetadataStore:
    mlmd_store = store.connect(address)
    _ = get_or_create_seldon_artifact_types(mlmd_store)
    return mlmd_store


def get_or_create_seldon_artifact_types(mlmd_store: mlmd.metadata_store.MetadataStore):
    artifact_types = {}
    for name, properties in schemas.MLMD_artifact_TYPES.items():
        at = store.get_or_create_artifact_type(mlmd_store, name, properties)
        artifact_types[at.name] = at
    return artifact_types


def save_seldon_model_to_store(
    mlmd_store: mlmd.metadata_store.MetadataStore, seldon_model: schemas.Model
) -> metadata_store_pb2.Artifact:
    artifact = schemas.seldon_model_as_mlmd_artifact(seldon_model)
    return store.update_or_create_artifact(
        mlmd_store, schemas.SELDON_GRANULAR_MODEL, artifact
    )


def load_seldon_models_from_store(mlmd_store: mlmd.metadata_store.MetadataStore):
    artifacts = mlmd_store.get_artifacts_by_type(schemas.SELDON_GRANULAR_MODEL)
    models = [schemas.mlmd_artifact_as_seldon_model(a) for a in artifacts]
    return models
