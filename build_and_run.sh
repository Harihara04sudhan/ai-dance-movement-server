#!/bin/bash

# Build and test Docker image locally

set -e

echo "🏗️  Building Docker image..."
docker build -t dance-movement-analysis:latest .

echo "✅ Docker image built successfully"

echo "🧪 Running tests in container..."
docker run --rm dance-movement-analysis:latest python -m pytest test_movement_analyzer.py -v

echo "✅ Tests passed"

echo "🚀 Starting container..."
docker run -d \
    --name dance-analysis-server \
    -p 8000:8000 \
    -v $(pwd)/uploads:/app/uploads \
    -v $(pwd)/outputs:/app/outputs \
    dance-movement-analysis:latest

echo "✅ Container started"
echo "📡 API available at http://localhost:8000"
echo "📋 Check health: curl http://localhost:8000/health"
echo ""
echo "To stop: docker stop dance-analysis-server"
echo "To remove: docker rm dance-analysis-server"
