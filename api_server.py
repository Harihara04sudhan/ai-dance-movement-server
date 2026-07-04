"""
FastAPI Server for Dance Movement Analysis
Provides endpoints for video upload and analysis
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import hmac
import os
import time
import uuid
import shutil
from pathlib import Path
from typing import Dict
import logging
from datetime import datetime

from movement_analyzer import DanceMovementAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Dance Movement Analysis API",
    description="AI-powered dance movement analysis using MediaPipe",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security: API key auth, rate limiting, upload size guard ---------------
# Set API_KEY in the environment to require an X-API-Key header on /api/* routes.
# Health endpoints stay unauthenticated for load balancers.
API_KEY = os.getenv("API_KEY", "")
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "100")) * 1024 * 1024
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "30"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

_request_log: Dict[str, list] = {}

OPEN_PATHS = {"/", "/health", "/docs", "/openapi.json"}


@app.middleware("http")
async def security_middleware(request, call_next):
    path = request.url.path

    if path in OPEN_PATHS:
        return await call_next(request)

    # API key auth (only enforced when API_KEY is configured)
    if API_KEY:
        provided = request.headers.get("x-api-key", "")
        if not hmac.compare_digest(provided, API_KEY):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing X-API-Key header"},
            )

    # In-memory sliding-window rate limit per client IP
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = _request_log.setdefault(client_ip, [])
    window[:] = [t for t in window if now - t < RATE_LIMIT_WINDOW]
    if len(window) >= RATE_LIMIT_REQUESTS:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
        )
    window.append(now)

    # Reject oversized uploads before reading the body
    if path == "/api/analyze":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_UPLOAD_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail": f"Upload too large (max {MAX_UPLOAD_BYTES // (1024 * 1024)} MB)"},
            )

    return await call_next(request)


# Setup directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Store job statuses
job_status: Dict[str, dict] = {}

# Initialize analyzer
analyzer = DanceMovementAnalyzer()


def cleanup_old_files():
    """Remove files older than 1 hour"""
    import time
    current_time = time.time()
    for directory in [UPLOAD_DIR, OUTPUT_DIR]:
        for file_path in directory.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > 3600:  # 1 hour
                    file_path.unlink()
                    logger.info(f"Cleaned up old file: {file_path}")


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Dance Movement Analysis API started")
    if not API_KEY:
        logger.warning(
            "API_KEY is not set — /api/* endpoints are UNAUTHENTICATED. "
            "Set the API_KEY environment variable before deploying publicly."
        )
    cleanup_old_files()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Dance Movement Analysis API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "uploads_dir": str(UPLOAD_DIR.absolute()),
        "outputs_dir": str(OUTPUT_DIR.absolute()),
        "active_jobs": len(job_status)
    }


def process_video_task(job_id: str, input_path: str, output_path: str):
    """Background task to process video"""
    try:
        job_status[job_id]["status"] = "processing"
        job_status[job_id]["started_at"] = datetime.now().isoformat()
        
        logger.info(f"Starting analysis for job {job_id}")
        
        # Analyze the video
        success, message, stats = analyzer.analyze_video(input_path, output_path)
        
        if success:
            job_status[job_id]["status"] = "completed"
            job_status[job_id]["statistics"] = stats
            job_status[job_id]["output_file"] = os.path.basename(output_path)
            logger.info(f"Job {job_id} completed successfully")
        else:
            job_status[job_id]["status"] = "failed"
            job_status[job_id]["error"] = message
            logger.error(f"Job {job_id} failed: {message}")
        
        job_status[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        job_status[job_id]["status"] = "failed"
        job_status[job_id]["error"] = str(e)
        job_status[job_id]["completed_at"] = datetime.now().isoformat()


@app.post("/api/analyze")
async def analyze_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...)
):
    """
    Upload a dance video for movement analysis
    
    Returns:
        job_id for tracking the analysis progress
    """
    # Validate file type (check both content type and extension)
    valid_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    is_valid_type = (video.content_type and video.content_type.startswith("video/")) or \
                    video.filename.lower().endswith(valid_extensions)
    
    if not is_valid_type:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload a video file (mp4, avi, mov, etc.)."
        )
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    input_filename = f"{job_id}_input{Path(video.filename).suffix}"
    input_path = UPLOAD_DIR / input_filename
    
    output_filename = f"{job_id}_output.mp4"
    output_path = OUTPUT_DIR / output_filename
    
    try:
        # Save uploaded video
        with input_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        logger.info(f"Video uploaded for job {job_id}: {video.filename}")
        
        # Initialize job status
        job_status[job_id] = {
            "status": "queued",
            "original_filename": video.filename,
            "created_at": datetime.now().isoformat(),
            "input_file": input_filename,
            "output_file": None
        }
        
        # Add background task
        background_tasks.add_task(
            process_video_task, 
            job_id, 
            str(input_path), 
            str(output_path)
        )
        
        return JSONResponse(
            status_code=202,
            content={
                "job_id": job_id,
                "status": "queued",
                "message": "Video uploaded successfully. Analysis started."
            }
        )
        
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        if input_path.exists():
            input_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing upload: {str(e)}")


@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    """
    Get the status of a video analysis job
    
    Args:
        job_id: The unique job identifier
        
    Returns:
        Current status and details of the job
    """
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_status[job_id]


@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    """
    Download the analyzed video result
    
    Args:
        job_id: The unique job identifier
        
    Returns:
        The processed video file with skeleton overlay
    """
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_status[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Job status: {job['status']}. Result not available yet."
        )
    
    output_file = OUTPUT_DIR / job["output_file"]
    
    if not output_file.exists():
        raise HTTPException(status_code=404, detail="Result file not found")
    
    return FileResponse(
        path=output_file,
        media_type="video/mp4",
        filename=f"analyzed_{job['original_filename']}"
    )


@app.delete("/api/job/{job_id}")
async def delete_job(job_id: str):
    """
    Delete a job and its associated files
    
    Args:
        job_id: The unique job identifier
    """
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_status[job_id]
    
    # Delete input file
    if job.get("input_file"):
        input_path = UPLOAD_DIR / job["input_file"]
        if input_path.exists():
            input_path.unlink()
    
    # Delete output file
    if job.get("output_file"):
        output_path = OUTPUT_DIR / job["output_file"]
        if output_path.exists():
            output_path.unlink()
    
    # Remove from status
    del job_status[job_id]
    
    return {"message": "Job deleted successfully"}


@app.get("/api/jobs")
async def list_jobs():
    """
    List all jobs
    
    Returns:
        List of all jobs with their current status
    """
    return {
        "total_jobs": len(job_status),
        "jobs": job_status
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "api_server:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True
    )
