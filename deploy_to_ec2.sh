#!/bin/bash

# ============================================================
# 🚀 EC2 Deployment Script for Volunteer Predictor App
# ============================================================

# Configuration
EC2_IP="13.232.52.36"
KEY_PATH="/Users/harshk/CodeSpace/OPS/volunteer-app-key.pem"
ECR_REPO="632676638228.dkr.ecr.ap-south-1.amazonaws.com/volunteer-predictor"
AWS_REGION="ap-south-1"

echo "════════════════════════════════════════════"
echo "🚀 Deploying Latest Model to EC2 ($EC2_IP)"
echo "════════════════════════════════════════════"
echo ""

# SSH into EC2 and deploy
ssh -i "$KEY_PATH" ubuntu@"$EC2_IP" << 'ENDSSH'
    set -e

    echo "1️⃣  Logging into AWS ECR..."
    aws ecr get-login-password --region ap-south-1 | \
        sudo docker login --username AWS --password-stdin \
        632676638228.dkr.ecr.ap-south-1.amazonaws.com

    echo ""
    echo "2️⃣  Stopping old container..."
    sudo docker stop volunteer-app 2>/dev/null || echo "   No container running"
    sudo docker rm volunteer-app 2>/dev/null || echo "   No container to remove"

    echo ""
    echo "3️⃣  Pulling latest Docker image..."
    sudo docker pull 632676638228.dkr.ecr.ap-south-1.amazonaws.com/volunteer-predictor:latest

    echo ""
    echo "4️⃣  Starting new container..."
    sudo docker run -d \
        -p 5000:5000 \
        --restart unless-stopped \
        --name volunteer-app \
        632676638228.dkr.ecr.ap-south-1.amazonaws.com/volunteer-predictor:latest

    echo ""
    echo "5️⃣  Waiting for application to start..."
    sleep 15

    echo ""
    echo "6️⃣  Checking health endpoint..."
    curl -s http://localhost:5000/health | python3 -m json.tool || echo "Health check failed"

    echo ""
    echo "7️⃣  Checking version endpoint..."
    curl -s http://localhost:5000/version | python3 -m json.tool || echo "Version check failed"

    echo ""
    echo "8️⃣  Checking model info endpoint..."
    curl -s http://localhost:5000/model-info | python3 -m json.tool || echo "Model info check failed"

ENDSSH

echo ""
echo "════════════════════════════════════════════"
echo "✅ Deployment Complete!"
echo "════════════════════════════════════════════"
echo ""
echo "🌐 Access your app at: http://$EC2_IP:5000"
echo ""

