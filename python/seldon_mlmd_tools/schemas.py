import json

from pydantic import BaseModel
from typing import List, Dict, Union, Tuple, Literal

from ml_metadata.proto import metadata_store_pb2


################################ Seldon Schemas ###############################


class PydanticBase(BaseModel):
    class Config:
        validate_assignment = True


# TODO: Decide if we really need a different classes for each of the feature type


class OrdinalFeature(PydanticBase):
    name: str
    dtype: str
    qdtype: Literal["ordinal"]
    stats: Dict[str, int] = None


class CategoricalFeature(PydanticBase):
    name: str
    dtype: str
    qdtype: Literal["categorical"]
    n_categories: int
    category_map: Dict[int, str]


class OneHotCategoricalFeature(PydanticBase):
    name: str
    dtype: str
    qdtype: Literal["one-hot-categorical"]
    category_name: str
    categorical_variable_id: int


class DefaultFeature(PydanticBase):
    name: str
    dtype: str
    qdtype: str


class DataSchema(PydanticBase):
    type: str
    features: List[
        Union[
            OrdinalFeature, CategoricalFeature, OneHotCategoricalFeature, DefaultFeature
        ]
    ]


class Model(PydanticBase):
    name: str = None
    type: str = None
    task: str = None
    input_schema: DataSchema = None
    output_schema: DataSchema = None


########################## MLMD Artifact Types ################################

SELDON_GRANULAR_MODEL = "SeldonGranularModel"

MLMD_artifact_TYPES = {
    SELDON_GRANULAR_MODEL: {
        "type": metadata_store_pb2.STRING,
        "task": metadata_store_pb2.STRING,
        "input_data_schema": metadata_store_pb2.STRING,
        "output_data_schema": metadata_store_pb2.STRING,
    }
}


########################### Translation Layer #################################


def seldon_model_as_mlmd_artifact(model: Model) -> metadata_store_pb2.Artifact:
    """Convert Model schema to unsaved artifact.

    Note: both artifact's id and type_id are not set.
    """
    artifact = metadata_store_pb2.Artifact()
    artifact.name = model.name

    artifact.properties["type"].string_value = model.type
    artifact.properties["task"].string_value = model.task
    artifact.properties["input_data_schema"].string_value = model.input_schema.json()
    artifact.properties["output_data_schema"].string_value = model.output_schema.json()

    return artifact


def mlmd_artifact_as_seldon_model(artifact: metadata_store_pb2.Artifact) -> Model:
    model = Model(
        name=artifact.name,
        task=artifact.properties["task"].string_value,
        type=artifact.properties["type"].string_value,
        input_schema=json.loads(artifact.properties["input_data_schema"].string_value),
        output_schema=json.loads(
            artifact.properties["output_data_schema"].string_value
        ),
    )
    return model
