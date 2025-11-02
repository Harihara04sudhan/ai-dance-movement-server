#!/bin/bash

# Deploy to GCP Compute Engine
# Prerequisites:
# - gcloud CLI configured
# - GCP project set up
# - Compute Engine instance running

set -e

# Configuration
GCP_PROJECT="${GCP_PROJECT:-your-project-id}"
GCP_INSTANCE="${GCP_INSTANCE:-dance-analysis-instance}"
GCP_ZONE="${GCP_ZONE:-us-central1-a}"
DOCKER_IMAGE="dance-movement-analysis"

echo "🚀 Deploying to GCP Compute Engine..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t $DOCKER_IMAGE:latest .

# Tag for GCP Container Registry
echo "🏷️  Tagging image for GCR..."
docker tag $DOCKER_IMAGE:latest gcr.io/$GCP_PROJECT/$DOCKER_IMAGE:latest

# Push to GCR
echo "📤 Pushing to Google Container Registry..."
docker push gcr.io/$GCP_PROJECT/$DOCKER_IMAGE:latest

# Deploy to Compute Engine
echo "🔧 Deploying to Compute Engine..."
gcloud compute ssh $GCP_INSTANCE --zone=$GCP_ZONE --project=$GCP_PROJECT --command="
    # Pull latest image
    docker pull gcr.io/$GCP_PROJECT/$DOCKER_IMAGE:latest
    
    # Stop and remove old container
    docker stop dance-analysis-api 2>/dev/null || true
    docker rm dance-analysis-api 2>/dev/null || true
    
    # Run new container
    docker run -d \
        --name dance-analysis-api \
        --restart unless-stopped \
        -p 80:8000 \
        -v ~/uploads:/app/uploads \
        -v ~/outputs:/app/outputs \
        gcr.io/$GCP_PROJECT/$DOCKER_IMAGE:latest
    
    echo '✅ Deployment complete'
"

echo "✅ Deployment successful!"
echo "🌐 Get instance IP: gcloud compute instances describe $GCP_INSTANCE --zone=$GCP_ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)'"
