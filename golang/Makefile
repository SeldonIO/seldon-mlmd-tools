compile_mlmd_protos:
	git clone -b r0.25.0 https://github.com/google/ml-metadata.git ml-metadata-source
	cd ml-metadata-source && protoc --go_out=plugins=grpc:. --go_opt=paths=source_relative \
		ml_metadata/proto/metadata_store.proto \
		ml_metadata/proto/metadata_store_service.proto
	cd ml-metadata-source/ml_metadata/proto && \
		cp metadata_store.* metadata_store_service.* \
	   ../../../proto/ml_metadata/
	rm -rf ml-metadata-source
