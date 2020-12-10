package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	pb "github.com/seldonio/seldon-mlmd-tools/golang/proto/ml_metadata"
	schemas "github.com/seldonio/seldon-mlmd-tools/golang/schemas"
	"google.golang.org/grpc"
)

const (
	address          = "localhost:8080"
	artifactTypeName = "SeldonGranularModel"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewMetadataStoreServiceClient(conn)

	// Contact the server and print out its response.
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	typeName := artifactTypeName

	getArtifactsResponse, err := c.GetArtifactsByType(ctx, &pb.GetArtifactsByTypeRequest{TypeName: &typeName})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}

	artifacts := getArtifactsResponse.GetArtifacts()

	for n, artifact := range artifacts {
		fmt.Println("Artifact number", n, "named:", *artifact.Name)
		meta := schemas.NewGranularModelMetadataFromArtifact(artifact)

		// PrettyPrint it
		res, _ := json.MarshalIndent(meta, "", "    ")
		fmt.Println(string(res))
	}
}
