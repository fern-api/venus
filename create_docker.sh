

#!/usr/bin/env bash

set -e

TAG="$1"
DOCKER_NAME=venus:"$TAG"

PACKAGE_DIR="$DOCKER_DIR/.."

docker build -f Dockerfile -t "$DOCKER_NAME" .

docker save "$DOCKER_NAME" -o "$DOCKER_NAME.tar"

echo
echo "Built docker: $DOCKER_NAME"
echo "To run image: docker run $DOCKER_NAME"
echo
