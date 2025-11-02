# 🎥 Demo Video Recording Guide

This guide will help you create a professional 2-minute demonstration video for the Dance Movement Analysis project.

## 📋 Pre-Recording Checklist

- [ ] Server is running (locally or on cloud)
- [ ] Sample dance video ready for upload
- [ ] Screen recording software ready (OBS Studio, QuickTime, etc.)
- [ ] Clear your desktop/browser tabs
- [ ] Test your audio/microphone
- [ ] Have the API endpoint URL ready

## 🎬 Video Structure (2 minutes)

### Introduction (15 seconds)
**What to show:**
- Brief project title card
- Your name and the Callus Company Inc. logo

**What to say:**
```
"Hello, I'm [Your Name]. This is my Dance Movement Analysis API project for 
Callus Company Inc. - an AI-powered cloud-based server that analyzes body 
movements from dance videos using MediaPipe and computer vision."
```

### Part 1: Project Overview (20 seconds)
**What to show:**
- README file opened in editor
- Quick scroll through the documentation

**What to say:**
```
"The project uses Python, FastAPI, MediaPipe, and OpenCV to detect body 
keypoints and overlay a skeleton visualization on dance videos. It's fully 
containerized with Docker and deployed to the cloud."
```

### Part 2: Code Walkthrough (25 seconds)
**What to show:**
- Open `movement_analyzer.py` and scroll through key sections
- Highlight the MediaPipe integration
- Show the test file briefly

**What to say:**
```
"The core analyzer uses MediaPipe Pose to detect 33 body keypoints with high 
accuracy. The code includes comprehensive unit tests and follows production-ready 
practices with proper error handling and logging."
```

### Part 3: API Demonstration (40 seconds)
**What to show:**
- Browser or Postman showing the API
- Upload a sample dance video
- Show the job_id response

**What to say:**
```
"Let me demonstrate the API. I'm uploading a dance video to the /api/analyze 
endpoint. The server returns a job ID immediately as it processes the video 
asynchronously in the background."
```

**What to show:**
- Check status endpoint multiple times
- Show the statistics when completed

**What to say:**
```
"We can check the processing status. As you can see, it's analyzing the frames. 
The analysis is now complete with a 98% detection rate and detailed statistics."
```

### Part 4: Result Showcase (30 seconds)
**What to show:**
- Download the result video
- Play the analyzed video side-by-side with original
- Highlight the skeleton overlay tracking the dancer

**What to say:**
```
"Here's the result - the analyzed video with the skeleton overlay perfectly 
tracking the dancer's movements. The skeleton accurately captures all body 
keypoints in real-time, even during complex dance moves."
```

### Part 5: Deployment & Cloud (20 seconds)
**What to show:**
- Show Docker container running
- Show the deployment scripts
- If deployed to cloud, show the cloud console/instance

**What to say:**
```
"The application is fully containerized with Docker and deployed to [AWS/GCP]. 
I've included automated deployment scripts for both AWS EC2 and GCP Compute 
Engine, making it production-ready."
```

### Conclusion (10 seconds)
**What to show:**
- GitHub repository page
- README overview

**What to say:**
```
"All code, tests, and documentation are available in the GitHub repository. 
This project aligns with Callus's vision of scalable, AI-powered solutions. 
Thank you for watching!"
```

## 🛠️ Technical Setup

### Screen Recording Settings
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 FPS
- **Audio**: Clear voice narration
- **Format**: MP4 (H.264 codec)

### Recommended Tools
- **OBS Studio** (Free, cross-platform)
- **QuickTime** (Mac)
- **Windows Game Bar** (Windows)
- **SimpleScreenRecorder** (Linux)

### Camera Position (if showing face)
- Professional background
- Good lighting
- Eye level camera position

## 📝 Script Tips

1. **Practice First**: Do a dry run before recording
2. **Speak Clearly**: Enunciate and maintain good pace
3. **Show, Don't Just Tell**: Demonstrate features actively
4. **Time Management**: Keep each section within time limits
5. **Professional Tone**: Confident but not arrogant

## 🎨 Visual Elements to Include

### Terminal/Console Commands
```bash
# Show these commands in action
docker build -t dance-movement-analysis .
docker run -p 8000:8000 dance-movement-analysis
curl -X POST http://localhost:8000/api/analyze -F "video=@dance.mp4"
```

### API Endpoints to Demonstrate
- `GET /health` - Show the API is healthy
- `POST /api/analyze` - Upload video
- `GET /api/status/{job_id}` - Check progress
- `GET /api/result/{job_id}` - Download result

### Code Snippets to Highlight
- MediaPipe initialization in `movement_analyzer.py`
- FastAPI endpoint in `api_server.py`
- Test cases in `test_movement_analyzer.py`
- Dockerfile configuration

## ✅ Quality Checklist

Before finalizing the video:
- [ ] Audio is clear and professional
- [ ] No background noise or distractions
- [ ] All demonstrations work smoothly
- [ ] Video is exactly 2 minutes (±5 seconds)
- [ ] Screen text is readable at 1080p
- [ ] Transitions are smooth
- [ ] No sensitive information visible (API keys, passwords)
- [ ] Final export is in MP4 format
- [ ] File size is reasonable (< 100MB)

## 🎯 Sample Recording Timeline

| Time | Section | Content |
|------|---------|---------|
| 0:00-0:15 | Intro | Title card, introduction |
| 0:15-0:35 | Overview | Project description, tech stack |
| 0:35-1:00 | Code | Show key code sections |
| 1:00-1:40 | Demo | Upload video, show processing, results |
| 1:40-2:00 | Conclusion | Deployment, GitHub, closing |

## 💡 Pro Tips

1. **Use Picture-in-Picture**: Show your face in corner while demoing
2. **Add Captions**: Help viewers follow along
3. **Use Zoom**: Zoom in on important details
4. **Smooth Transitions**: Use fade or cut transitions between sections
5. **Background Music**: Subtle, professional background music (optional)
6. **Test Upload**: Make sure the final video plays correctly

## 🚀 After Recording

1. **Edit**: Trim any mistakes or dead air
2. **Add Graphics**: Title cards, annotations
3. **Color Correction**: Ensure good contrast and visibility
4. **Audio Normalization**: Consistent audio levels
5. **Export**: MP4, H.264, 1920x1080, 30fps
6. **Review**: Watch it once more before submission
7. **Upload**: To your preferred platform or include in submission

## 📤 Submission Format

Save the final video as:
```
dance_movement_analysis_demo.mp4
```

Ensure the video:
- Is exactly in MP4 format
- Is around 2 minutes long
- Has clear audio and video
- Demonstrates all required features
- Shows the API endpoint URL
- Includes the GitHub repository URL

---

**Good luck with your recording! Remember: confidence, clarity, and demonstration are key!** 🎬
