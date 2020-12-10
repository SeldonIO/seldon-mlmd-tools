# Seldon MLMD Tools

This repository contains helper tools to handle Seldon metadata with MLMD.

> :warning: **NOTE:** This is work in progress!



## MLMD References

* [MLMD documentation](https://www.tensorflow.org/tfx/guide/mlmd)
* Kubeflow abstractions on top of mlmd: [kubeflow/metadata/.../metadata.py](https://github.com/kubeflow/metadata/blob/master/sdk/python/kubeflow/metadata/metadata.py)
* MLMD in Kubeflow pipelines: [kubeflow/pipelines/.../metadata_helpers.py](https://github.com/kubeflow/pipelines/blob/master/backend/metadata_writer/src/metadata_helpers.py)




## Python

### Environment notes

Environment is controlled by [poetry](https://python-poetry.org/).
One should be able to `pip install .` it by I recommend to try `poetry`.

### Installing environment

Without any virtual environment active executing
```bash
poetry install .
```
in this directory will create a new virtual environment for you, see details with
```bash
poetry info
```

### Starting notebook server

You can start `Jupyter Lab` server by executing
```bash
poetry run jupyter lab
```


## Golang

The initial Golang  code is located in [golang](./golang/) folder.



## Kubernetes (Kind) Deployment

Resources are defined in [k8s-deployment](./k8s-deployment) directory.
Use [Makefile](./k8s-deployment/Makefile) to create `kind` cluster and deploy MLMD Service:
```bash
make create-kind-cluster
make deploy-mlmd-grpc-service
```

To access mlmd from local machine (without configuring ingreess) just port-forward it with
```bash
kubectl port-forward -n mlmd-system svc/metadata-grpc-service 8080:8080
```
