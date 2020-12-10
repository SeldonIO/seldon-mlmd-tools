package schemas

import (
	"encoding/json"
	pb "github.com/seldonio/seldon-mlmd-tools/golang/proto/ml_metadata"
)

type FeatureMetadata interface {
	isFeatureMetadata()
}

type DefaultFeature struct {
	Name   string `json:"name"`
	DType  string `json:"dtype"`
	QDType string `json:"qdtype"`
}

func (*DefaultFeature) isFeatureMetadata() {}

type OrdinalFeature struct {
	Name   string         `json:"name"`
	DType  string         `json:"dtype"`
	QDType string         `json:"qdtype"`
	Stats  map[string]int `json:"stats"`
}

func (*OrdinalFeature) isFeatureMetadata() {}

type CategoricalFeature struct {
	Name        string         `json:"name"`
	DType       string         `json:"dtype"`
	QDType      string         `json:"qdtype"`
	NCategories int            `json:"n_categories"`
	CategoryMap map[int]string `json:"category_map"`
}

func (*CategoricalFeature) isFeatureMetadata() {}

type OneHotCategoricalFeature struct {
	Name               string `json:"name"`
	DType              string `json:"dtype"`
	QDType             string `json:"qdtype"`
	CategoryName       string `json:"category_name"`
	CategoryVariableId int    `json:"categorical_variable_id"`
}

func (*OneHotCategoricalFeature) isFeatureMetadata() {}

type DataSchema struct {
	Type     string            `json:"type"`
	Features []FeatureMetadata `json:"features"`
}

type RawDataSchema struct {
	Type     string            `json:"type"`
	Features []json.RawMessage `json:"features"`
}

func NewDataSchemaFromValue(value *pb.Value) *DataSchema {
	var rawDataSchema RawDataSchema
	json.Unmarshal([]byte(value.GetStringValue()), &rawDataSchema)

	features := make([]FeatureMetadata, 0, len(rawDataSchema.Features))
	for _, rawFeatureJson := range rawDataSchema.Features {

		var rawFeature map[string]interface{}
		json.Unmarshal([]byte(rawFeatureJson), &rawFeature)

		switch featureType := rawFeature["qdtype"].(string); featureType {
		case "ordinal":
			var feature OrdinalFeature
			json.Unmarshal([]byte(rawFeatureJson), &feature)
			features = append(features, &feature)
		case "categorical":
			var feature CategoricalFeature
			json.Unmarshal([]byte(rawFeatureJson), &feature)
			features = append(features, &feature)
		case "one-hot-categorical":
			var feature OneHotCategoricalFeature
			json.Unmarshal([]byte(rawFeatureJson), &feature)
			features = append(features, &feature)
		default:
			var feature DefaultFeature
			json.Unmarshal([]byte(rawFeatureJson), &feature)
			features = append(features, &feature)
		}

	}

	return &DataSchema{
		Type:     rawDataSchema.Type,
		Features: features,
	}
}

type GranularModelMetadata struct {
	ModelName        string      `json:"name"`
	ModelType        string      `json:"type"`
	ModelTask        string      `json:"task"`
	InputDataSchema  *DataSchema `json:"input_data_schema"`
	OutputDataSchema *DataSchema `json:"output_data_schema"`
}

func NewGranularModelMetadataFromArtifact(artifact *pb.Artifact) *GranularModelMetadata {
	properties := artifact.GetProperties()
	metadata := GranularModelMetadata{
		ModelName:        artifact.GetName(),
		ModelType:        properties["type"].GetStringValue(),
		ModelTask:        properties["task"].GetStringValue(),
		InputDataSchema:  NewDataSchemaFromValue(properties["input_data_schema"]),
		OutputDataSchema: NewDataSchemaFromValue(properties["output_data_schema"]),
	}

	return &metadata
}
