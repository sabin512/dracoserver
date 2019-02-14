#!/bin/sh
echo "Building iotowl container..."
docker build --tag=iotowl .
echo "Starting iotowl..."
docker run -dit -p 8080:80 iotowl
