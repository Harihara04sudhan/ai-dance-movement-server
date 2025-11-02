# 🚀 Getting Started Guide

This guide will walk you through setting up and testing the Dance Movement Analysis project before deployment.

## 📋 Prerequisites

Make sure you have the following installed:
- Python 3.11 or higher
- Docker and Docker Compose
- Git
- (Optional) AWS CLI or GCP Cloud SDK for cloud deployment

## 🔧 Step-by-Step Setup

### Step 1: Navigate to Project Directory

```bash
cd "/home/hari/Music/callus/AI ML Server Engineer/dance-movement-analysis"
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test the Movement Analyzer

First, let's run the unit tests to ensure everything works:

```bash
pytest test_movement_analyzer.py -v
```

### Step 5: Run the Server Locally

```bash
python api_server.py
```

The server should start at `http://localhost:8000`

Open another terminal and test the health endpoint:

```bash
curl http://localhost:8000/health
```

### Step 6: Test with a Sample Video

You need a sample dance video to test. You can:
1. Download a free dance video from YouTube using `yt-dlp`
2. Use your own dance video
3. Record a short test video

Example using the demo client:

```bash
# In a new terminal (keep the server running)
python demo_client.py your_dance_video.mp4
```

### Step 7: Docker Testing

Stop the local server (Ctrl+C), then build and run with Docker:

```bash
# Build Docker image
docker build -t dance-movement-analysis .

# Run container
docker run -d -p 8000:8000 --name dance-api dance-movement-analysis

# Test health endpoint
curl http://localhost:8000/health

# View logs
docker logs -f dance-api

# Stop container
docker stop dance-api
docker rm dance-api
```

Or use Docker Compose:

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Step 8: Prepare for Cloud Deployment

#### For AWS EC2:

1. Create an EC2 instance (Ubuntu 20.04+)
2. Install Docker on the instance
3. Configure security group to allow port 80
4. Update `deploy_aws.sh` with your instance details:

```bash
export EC2_HOST="your-instance.compute.amazonaws.com"
export EC2_USER="ubuntu"
export SSH_KEY="~/.ssh/your-key.pem"
```

5. Deploy:

```bash
./deploy_aws.sh
```

#### For GCP Compute Engine:

1. Create a Compute Engine instance
2. Enable Container Registry API
3. Update `deploy_gcp.sh` with your details:

```bash
export GCP_PROJECT="your-project-id"
export GCP_INSTANCE="dance-analysis-instance"
export GCP_ZONE="us-central1-a"
```

4. Deploy:

```bash
./deploy_gcp.sh
```

### Step 9: Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Dance Movement Analysis API"

# Add remote (create a GitHub repo first)
git remote add origin https://github.com/yourusername/dance-movement-analysis.git

# Push to GitHub
git push -u origin main
```

### Step 10: Record Demo Video

Follow the instructions in `VIDEO_GUIDE.md` to record your 2-minute demonstration video.

## 🎯 Quick Test Checklist

Before submitting, verify:

- [ ] Unit tests pass: `pytest test_movement_analyzer.py -v`
- [ ] Server runs locally: `python api_server.py`
- [ ] Health endpoint works: `curl http://localhost:8000/health`
- [ ] Can upload and process a video successfully
- [ ] Docker build succeeds: `docker build -t dance-movement-analysis .`
- [ ] Docker container runs: `docker run -p 8000:8000 dance-movement-analysis`
- [ ] Deployed to cloud (AWS or GCP)
- [ ] GitHub repository is public and complete
- [ ] README.md is comprehensive
- [ ] Demo video is recorded and ready

## 🐛 Troubleshooting

### Issue: Import errors with cv2 or mediapipe

**Solution**: Make sure you're using the virtual environment and all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Docker build fails with "no space left on device"

**Solution**: Clean up Docker:
```bash
docker system prune -a
```

### Issue: API returns 500 error when processing video

**Solution**: Check the logs for detailed error messages:
```bash
docker logs dance-api
# or
tail -f api.log  # if logging to file
```

### Issue: Video processing is too slow

**Solution**: 
- Use a smaller/shorter test video
- Reduce MediaPipe model complexity in `movement_analyzer.py` (change `model_complexity=2` to `1`)
- Use a more powerful cloud instance

### Issue: Can't connect to cloud deployment

**Solution**: 
- Check security group/firewall rules allow port 80
- Verify the instance is running
- Check Docker container is running on the instance: `docker ps`

## 📚 Additional Resources

- [MediaPipe Pose Documentation](https://google.github.io/mediapipe/solutions/pose.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [GCP Compute Engine Guide](https://cloud.google.com/compute/docs)

## 💡 Tips for Success

1. **Start Simple**: Test with a short (5-10 second) video first
2. **Check Logs**: Always check logs when something doesn't work
3. **Test Locally First**: Ensure everything works locally before deploying to cloud
4. **Use Git Commits**: Commit frequently with descriptive messages
5. **Document Everything**: If you make changes, update the README
6. **Time Management**: Allow time for the demo video recording and editing

## 🎓 Learning Outcomes

By completing this project, you've demonstrated:
- ✅ Python programming with AI/ML libraries
- ✅ REST API development with FastAPI
- ✅ Computer vision with MediaPipe and OpenCV
- ✅ Containerization with Docker
- ✅ Cloud deployment (AWS/GCP)
- ✅ Testing and documentation
- ✅ DevOps practices

---

**Ready to submit? Make sure you have:**
1. ✅ Public GitHub repository
2. ✅ Comprehensive README.md
3. ✅ 2-minute demo video (.mp4)
4. ✅ Working cloud deployment

**Good luck! 🚀**
