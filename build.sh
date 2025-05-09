#!/bin/bash

IMAGE_NAME="mlkbenjamin/ingress-generator:0.1.0"

docker build . -t $IMAGE_NAME
docker push $IMAGE_NAME