#!/bin/bash

# Deploy to AWS EC2
# Prerequisites: 
# - AWS CLI configured
# - EC2 instance running
# - SSH key available

set -e

# Configuration
EC2_HOST="${EC2_HOST:-your-ec2-instance.compute.amazonaws.com}"
EC2_USER="${EC2_USER:-ubuntu}"
SSH_KEY="${SSH_KEY:-~/.ssh/your-key.pem}"
DOCKER_IMAGE="dance-movement-analysis"
CONTAINER_NAME="dance-analysis-api"

echo "🚀 Deploying to AWS EC2..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t $DOCKER_IMAGE:latest .

# Save Docker image
echo "💾 Saving Docker image..."
docker save $DOCKER_IMAGE:latest | gzip > dance-analysis-image.tar.gz

# Copy to EC2
echo "📤 Uploading to EC2..."
scp -i $SSH_KEY dance-analysis-image.tar.gz $EC2_USER@$EC2_HOST:~

# Deploy on EC2
echo "🔧 Deploying on EC2..."
ssh -i $SSH_KEY $EC2_USER@$EC2_HOST << 'ENDSSH'
    # Load Docker image
    docker load < dance-analysis-image.tar.gz
    
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
        dance-movement-analysis:latest
    
    # Cleanup
    rm dance-analysis-image.tar.gz
    
    echo "✅ Deployment complete"
ENDSSH

# Cleanup local file
rm dance-analysis-image.tar.gz

echo "✅ Deployment successful!"
echo "🌐 API should be available at http://$EC2_HOST"
