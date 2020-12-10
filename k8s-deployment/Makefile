DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

KIND_NAME ?= mlmd-research


create-kind-cluster:
	kind create cluster --name ${KIND_NAME} --image kindest/node:v1.17.5


deploy-mlmd-grpc-service:
	kubectl create ns mlmd-system || echo "mlmd-system namespace already exists"

	kubectl apply -n mlmd-system -f mysql.yaml
	kubectl rollout -n mlmd-system status deployment.apps/mysql

	kubectl apply -n mlmd-system -f metadata-grpc-service.yaml


port-forward-mlmd:
	kubectl port-forward -n mlmd-system svc/metadata-grpc-service 8080:8080
