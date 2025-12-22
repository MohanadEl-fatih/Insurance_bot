#!/bin/bash
# Start Redis using docker-compose

cd "$(dirname "$0")/.."
docker-compose -f infra/docker-compose.yml up -d
echo "Redis started on port 6379"

