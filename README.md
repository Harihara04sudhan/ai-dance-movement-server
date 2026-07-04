# 🕺 Dance Movement Analysis API

[![CI](https://github.com/Harihara04sudhan/ai-dance-movement-server/actions/workflows/ci.yml/badge.svg)](https://github.com/Harihara04sudhan/ai-dance-movement-server/actions/workflows/ci.yml)

An AI-powered cloud-based server that analyzes body movements from dance videos using MediaPipe Pose Detection. Built with Python, FastAPI, Docker, and deployed to the cloud.

## 📋 Overview

This project provides a REST API for analyzing dance movements in videos. It uses Google's MediaPipe library to detect body keypoints and overlays a skeleton visualization on the original video, enabling users to visualize movement patterns and body pose in real-time.

## 🎯 Features

- **AI-Powered Pose Detection**: Uses MediaPipe Pose for accurate body keypoint detection
- **Skeleton Overlay**: Visualizes body movements with an animated skeleton overlay
- **REST API**: Simple endpoints for video upload and result retrieval
- **Asynchronous Processing**: Background task processing for handling multiple requests
- **Docker Containerized**: Fully containerized for easy deployment
- **Cloud-Ready**: Deployment scripts for AWS EC2 and GCP Compute Engine
- **Comprehensive Testing**: Unit tests for accuracy and reliability
- **Production-Ready**: Health checks, logging, and error handling

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ POST /api/analyze (upload video)
       ▼
┌─────────────────────┐
│   FastAPI Server    │
│   (api_server.py)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────┐
│  Movement Analyzer      │
│  (movement_analyzer.py) │
│  - MediaPipe Pose       │
│  - OpenCV Processing    │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────┐
│ Processed Video │
│ with Skeleton   │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- AWS CLI / GCP CLI (for cloud deployment)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Harihara04sudhan/ai-dance-movement-server.git
cd ai-dance-movement-server
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
python api_server.py
```

The server will start at `http://localhost:8000`

### Docker Deployment

1. **Build the Docker image**
```bash
docker build -t dance-movement-analysis .
```

2. **Run the container**
```bash
docker run -p 8000:8000 dance-movement-analysis
```

Or use the provided script:
```bash
chmod +x build_and_run.sh
./build_and_run.sh
```

### Using Demo Client

A demo client is provided for easy testing:

```bash
# Create a test video (optional)
python create_test_video.py

# Run the demo client
python demo_client.py test_dance.mp4 output_result.mp4
```

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Dance Movement Analysis API",
  "version": "1.0.0"
}
```

#### 2. Analyze Video
```http
POST /api/analyze
Content-Type: multipart/form-data
```

**Request:**
- `video`: Video file (mp4, avi, mov)

**Response:**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "queued",
  "message": "Video uploaded successfully. Analysis started."
}
```

#### 3. Check Job Status
```http
GET /api/status/{job_id}
```

**Response:**
```json
{
  "status": "completed",
  "original_filename": "dance.mp4",
  "created_at": "2025-11-01T10:00:00",
  "completed_at": "2025-11-01T10:01:30",
  "statistics": {
    "total_frames": 300,
    "processed_frames": 300,
    "detected_frames": 295,
    "detection_rate": 98.3,
    "avg_keypoints": 31.5
  }
}
```

#### 4. Download Result
```http
GET /api/result/{job_id}
```

Returns the processed video file with skeleton overlay.

#### 5. Delete Job
```http
DELETE /api/job/{job_id}
```

#### 6. List All Jobs
```http
GET /api/jobs
```

## 💻 Usage Examples

### Using cURL

```bash
# Upload a video
curl -X POST "http://localhost:8000/api/analyze" \
  -F "video=@dance_video.mp4"

# Check status
curl "http://localhost:8000/api/status/{job_id}"

# Download result
curl -O "http://localhost:8000/api/result/{job_id}"
```

### Using Python

```python
import requests

# Upload video
with open('dance_video.mp4', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files={'video': f}
    )
    job_id = response.json()['job_id']

# Check status
status = requests.get(f'http://localhost:8000/api/status/{job_id}')
print(status.json())

# Download result when ready
if status.json()['status'] == 'completed':
    result = requests.get(f'http://localhost:8000/api/result/{job_id}')
    with open('analyzed_dance.mp4', 'wb') as f:
        f.write(result.content)
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest test_movement_analyzer.py -v

# Run with coverage
pytest test_movement_analyzer.py --cov=movement_analyzer --cov-report=html
```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

1. **Configure AWS credentials**
```bash
aws configure
```

2. **Update deployment script**
Edit `deploy_aws.sh` with your EC2 instance details:
```bash
export EC2_HOST="your-instance.compute.amazonaws.com"
export EC2_USER="ubuntu"
export SSH_KEY="~/.ssh/your-key.pem"
```

3. **Deploy**
```bash
chmod +x deploy_aws.sh
./deploy_aws.sh
```

### GCP Compute Engine Deployment

1. **Configure GCP**
```bash
gcloud init
gcloud auth login
```

2. **Update deployment script**
Edit `deploy_gcp.sh` with your GCP details:
```bash
export GCP_PROJECT="your-project-id"
export GCP_INSTANCE="dance-analysis-instance"
export GCP_ZONE="us-central1-a"
```

3. **Deploy**
```bash
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

## 🤔 Design Decisions & Thought Process

### Technology Choices

**MediaPipe over OpenCV DNN**: 
- MediaPipe provides superior accuracy for pose estimation
- Optimized for real-time performance
- Comprehensive 33-point body landmark model
- Better handling of occlusions and challenging poses

**FastAPI over Flask**:
- Async support for handling multiple video processing requests
- Automatic API documentation (Swagger/OpenAPI)
- Type hints and validation with Pydantic
- Better performance for I/O-bound operations

**Background Task Processing**:
- Video processing is CPU-intensive and time-consuming
- Async processing prevents request timeout
- Allows users to check status and retrieve results when ready
- Scales better for multiple concurrent requests

**Docker Containerization**:
- Ensures consistent environment across development and production
- Simplifies dependency management
- Easy deployment to any cloud platform
- Portable and reproducible builds

### Architecture Decisions

**Stateful Job Tracking**:
- In-memory job status storage for quick lookups
- Could be extended to Redis/database for production scale
- Automatic cleanup of old files to manage storage

**RESTful API Design**:
- Standard HTTP methods (GET, POST, DELETE)
- Clear resource naming (/api/analyze, /api/status, /api/result)
- Proper status codes (202 for accepted, 404 for not found)

**Error Handling & Logging**:
- Comprehensive error messages for debugging
- Structured logging for production monitoring
- Graceful degradation on detection failures

## 🎯 Alignment with Callus's Vision

This project demonstrates key competencies that align with Callus's focus on innovative AI/ML solutions:

1. **AI/ML Integration**: Practical application of computer vision and pose estimation for real-world use cases (dance analysis, fitness tracking, motion capture)

2. **Cloud-Native Architecture**: Built with scalability and cloud deployment in mind, following modern DevOps practices

3. **Production-Ready Code**: 
   - Comprehensive testing
   - Proper error handling
   - Documentation
   - Monitoring and health checks

4. **Developer Experience**: Clear API design, extensive documentation, and easy deployment make it accessible for both developers and end-users

5. **Extensibility**: The modular architecture allows for easy addition of features like:
   - Multiple person detection
   - Movement quality scoring
   - Comparison with reference videos
   - Real-time streaming analysis

## 📁 Project Structure

```
ai-dance-movement-server/
├── api_server.py              # FastAPI REST API server
├── movement_analyzer.py       # MediaPipe pose detection logic
├── test_movement_analyzer.py  # Comprehensive unit tests
├── demo_client.py             # Demo client for testing
├── create_test_video.py       # Test video generator
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── .gitignore                 # Git ignore patterns
├── .env.example               # Environment variables template
├── build_and_run.sh          # Local Docker build script
├── deploy_aws.sh             # AWS deployment script
├── deploy_gcp.sh             # GCP deployment script
├── README.md                 # Project documentation
├── GETTING_STARTED.md        # Quick start guide
├── VIDEO_GUIDE.md            # Video recording instructions
├── SUBMISSION_CHECKLIST.md   # Submission checklist
├── TEST_RESULTS.md           # Testing documentation
├── FINAL_SUBMISSION_GUIDE.md # Complete submission guide
├── DEMO_VIDEO_SCRIPT.md      # Video demo script
├── test_dance.mp4            # Sample test video
├── uploads/                  # Uploaded videos directory
└── outputs/                  # Processed videos directory
```

## 🔒 Security Considerations

- Input validation for uploaded files
- File type checking (video formats only)
- Automatic cleanup of old files
- Rate limiting recommended for production
- CORS configured (adjust for production)
- Environment variable support for sensitive config

## 🚀 Future Enhancements

- [ ] Support for real-time video streaming
- [ ] Multiple person detection in group dances
- [ ] Movement quality scoring algorithm
- [ ] Comparison with reference dance videos
- [ ] Export keypoint data in JSON format
- [ ] Integration with cloud storage (S3, GCS)
- [ ] WebSocket support for real-time progress updates
- [ ] GPU acceleration for faster processing
- [ ] Kubernetes deployment manifests

## 📝 License

MIT License

Copyright (c) 2025 Harihara Sudhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 👤 Author

**Harihara Sudhan**
- GitHub: [@Harihara04sudhan](https://github.com/Harihara04sudhan)
- Repository: [ai-dance-movement-server](https://github.com/Harihara04sudhan/ai-dance-movement-server)
- LinkedIn: [Connect with me](https://linkedin.com/in/harihara-sudhan)

**Project Details:**
- Created for: Callus Company Inc. Assessment
- Position: AI/ML Server Engineer
- Submission Date: November 2025
- Technologies: Python, MediaPipe, FastAPI, Docker, Computer Vision

## 🙏 Acknowledgments

- Google MediaPipe team for the excellent pose detection library
- FastAPI community for the modern web framework
- OpenCV contributors for computer vision tools

---

**Note**: This is a competency assessment project for Callus Company Inc., demonstrating AI/ML server development and cloud deployment skills.
