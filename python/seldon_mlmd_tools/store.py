# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Store interface is heavily based on Kubeflow/piplines metadata_helper.py, see original code at:
# https://github.com/kubeflow/pipelines/blob/master/backend/metadata_writer/src/metadata_helpers.py


import logging
import time


import ml_metadata as mlmd
from ml_metadata.proto import metadata_store_pb2


def value_to_mlmd_value(value) -> metadata_store_pb2.Value:
    if value is None:
        return metadata_store_pb2.Value()
    if isinstance(value, int):
        return metadata_store_pb2.Value(int_value=value)
    if isinstance(value, float):
        return metadata_store_pb2.Value(double_value=value)
    return metadata_store_pb2.Value(string_value=str(value))


def connect(address: str = None) -> mlmd.metadata_store.MetadataStore:

    if address is None:
        # If address is None we will use a fake in memory database for testing
        logging.info("Using in memory database.")
        connection_config = metadata_store_pb2.ConnectionConfig()
        connection_config.fake_database.SetInParent()
        return mlmd.metadata_store.MetadataStore(connection_config)
    else:
        logging.info("Connecting to database at {address}")
        host, port = address.split(":")

        mlmd_connection_config = metadata_store_pb2.MetadataStoreClientConfig(
            host=host,
            port=int(port),
        )

    # Checking the connection to the Metadata store.
    for _ in range(100):
        try:
            return mlmd.metadata_store.MetadataStore(mlmd_connection_config)
        except Exception as e:
            logging.error(f'Failed to access the Metadata store. Exception: "{e}"')
            time.sleep(1)

    raise RuntimeError("Could not connect to the Metadata store.")


def get_or_create_artifact_type(
    store: mlmd.metadata_store.MetadataStore, type_name: str, properties: dict = None
) -> metadata_store_pb2.ArtifactType:
    try:
        artifact_type = store.get_artifact_type(type_name=type_name)
        return artifact_type
    except:
        artifact_type = metadata_store_pb2.ArtifactType(
            name=type_name,
            properties=properties,
        )
        artifact_type.id = store.put_artifact_type(artifact_type)  # Returns ID
        return artifact_type


def update_or_create_artifact(
    store: mlmd.metadata_store.MetadataStore,
    type_name: str,
    artifact: metadata_store_pb2.Artifact,
) -> metadata_store_pb2.Artifact:
    # We assume that type already exists in database
    artifact_type = store.get_artifact_type(type_name=type_name)

    # This will be None if artifact does not exist
    existing_artifact = store.get_artifact_by_type_and_name(
        artifact_type.name, artifact.name
    )

    if existing_artifact is not None:
        artifact.id = existing_artifact.id

    artifact.type_id = artifact_type.id
    artifact.id = store.put_artifacts([artifact])[0]
    return artifact
