# Golang Client to the MLMD metadata store that understand Seldon Schemas


First working code. WIP.

## Example

Requirements:
- grpc server deployed, see `k8s-deployment` in parent directory
- port 8080 is port-forwarded to mlmd grpc service
- run python examples first


```bash
╭─rskolasinski at machine42
╰─λ go run golang_tools/client.go
Artifact number 0 named: MyBlackBoxModel
{
    "name": "MyBlackBoxModel",
    "type": "blackbox",
    "task": "classification",
    "input_data_schema": {
        "type": "tabular",
        "features": [
            {
                "name": "age",
                "dtype": "int",
                "qdtype": "ordinal",
                "stats": {
                    "max": 70,
                    "min": 18
                }
            },
            {
                "name": "occupation",
                "dtype": "int",
                "qdtype": "categorical",
                "n_categories": 3,
                "category_map": {
                    "0": "Blue Collar",
                    "1": "White Collar",
                    "2": "Other"
                }
            },
            {
                "name": "sex",
                "dtype": "str",
                "qdtype": "one-hot-categorical",
                "category_name": "male",
                "categorical_variable_id": 1
            },
            {
                "name": "sex",
                "dtype": "str",
                "qdtype": "one-hot-categorical",
                "category_name": "female",
                "categorical_variable_id": 1
            }
        ]
    },
    "output_data_schema": {
        "type": "tabular",
        "features": [
            {
                "name": "accept",
                "dtype": "float",
                "qdtype": "proba"
            },
            {
                "name": "reject",
                "dtype": "float",
                "qdtype": "proba"
            }
        ]
    }
}
```
