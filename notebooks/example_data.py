input_schema = {
    "type": "tabular",  # 2D implied
    "features": [
        {
            "name": "age",
            "dtype": "int",  # float
            "qdtype": "ordinal",  # real, pos
            "stats": {
                "min": 18,
                "max": 70,
            },
        },
        {
            "name": "occupation",
            "dtype": "int",  # str
            "qdtype": "categorical",
            "n_categories": 3,
            "category_map": {0: "Blue Collar", 1: "White Collar", 2: "Other"},
        },
        {
            "name": "sex",
            "dtype": "str",  # int, bool
            "qdtype": "one-hot-categorical",
            "category_name": "male",
            "categorical_variable_id": 1,
        },
        {
            "name": "sex",
            "dtype": "str",  # int, bool
            "qdtype": "one-hot-categorical",
            "category_name": "female",
            "categorical_variable_id": 1,
        },
    ],
}


output_schema = {
    "type": "tabular",
    "features": [
        {
            "name": "accept",
            "dtype": "float",
            "qdtype": "proba",
        },
        {
            "name": "reject",
            "dtype": "float",
            "qdtype": "proba",
        },
    ],
}


model_schema = {
    "name": "MyBlackBoxModel",
    "type": "blackbox",
    "task": "classification",
    "output_schema": output_schema,
    "input_schema": input_schema,
}
