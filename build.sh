#!/bin/bash

# Build the Docker image
docker build -t noah-output-optimizer-addon .

# Tag the Docker image
docker tag noah-output-optimizer-addon YOUR_DOCKER_HUB_USERNAME/noah-output-optimizer-addon:latest

# Push the Docker image to Docker Hub
docker push YOUR_DOCKER_HUB_USERNAME/noah-output-optimizer-addon:latest
