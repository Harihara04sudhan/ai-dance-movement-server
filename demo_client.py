"""
Demo client for testing the Dance Movement Analysis API
Shows how to upload a video, track progress, and download results
"""

import requests
import time
import sys
from pathlib import Path


class DanceAnalysisClient:
    """Client for interacting with the Dance Movement Analysis API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self):
        """Check if the API is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return None
    
    def upload_video(self, video_path: str):
        """Upload a video for analysis"""
        try:
            with open(video_path, 'rb') as f:
                files = {'video': f}
                response = requests.post(
                    f"{self.base_url}/api/analyze",
                    files=files
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def get_status(self, job_id: str):
        """Get the status of a job"""
        try:
            response = requests.get(f"{self.base_url}/api/status/{job_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return None
    
    def download_result(self, job_id: str, output_path: str):
        """Download the analyzed video"""
        try:
            response = requests.get(f"{self.base_url}/api/result/{job_id}")
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def wait_for_completion(self, job_id: str, timeout: int = 300, poll_interval: int = 2):
        """Wait for a job to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_status(job_id)
            
            if not status:
                return None
            
            current_status = status.get('status')
            
            if current_status == 'completed':
                return status
            elif current_status == 'failed':
                print(f"❌ Job failed: {status.get('error', 'Unknown error')}")
                return status
            
            # Show progress
            if 'statistics' in status:
                stats = status['statistics']
                if 'processed_frames' in stats and 'total_frames' in stats:
                    progress = (stats['processed_frames'] / stats['total_frames']) * 100
                    print(f"⏳ Processing... {progress:.1f}% complete", end='\r')
            else:
                print(f"⏳ Status: {current_status}", end='\r')
            
            time.sleep(poll_interval)
        
        print(f"\n⚠️  Timeout waiting for job completion")
        return None


def main():
    """Main demo function"""
    if len(sys.argv) < 2:
        print("Usage: python demo_client.py <video_file> [output_file]")
        print("\nExample:")
        print("  python demo_client.py dance_video.mp4")
        print("  python demo_client.py dance_video.mp4 analyzed_output.mp4")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else "analyzed_output.mp4"
    
    # Validate input file
    if not Path(input_video).exists():
        print(f"❌ Input video not found: {input_video}")
        sys.exit(1)
    
    print("🕺 Dance Movement Analysis Demo Client")
    print("=" * 50)
    
    # Initialize client
    client = DanceAnalysisClient()
    
    # Health check
    print("\n1️⃣  Checking API health...")
    health = client.health_check()
    if not health:
        print("❌ API is not available. Make sure the server is running.")
        sys.exit(1)
    print(f"✅ API is healthy: {health.get('service', 'Unknown')}")
    
    # Upload video
    print(f"\n2️⃣  Uploading video: {input_video}")
    result = client.upload_video(input_video)
    if not result:
        print("❌ Failed to upload video")
        sys.exit(1)
    
    job_id = result['job_id']
    print(f"✅ Video uploaded successfully")
    print(f"   Job ID: {job_id}")
    
    # Wait for processing
    print("\n3️⃣  Waiting for analysis to complete...")
    status = client.wait_for_completion(job_id)
    
    if not status:
        print("\n❌ Analysis failed or timed out")
        sys.exit(1)
    
    if status['status'] != 'completed':
        print(f"\n❌ Job did not complete successfully: {status['status']}")
        sys.exit(1)
    
    # Show statistics
    print("\n\n✅ Analysis completed!")
    if 'statistics' in status:
        stats = status['statistics']
        print("\n📊 Statistics:")
        print(f"   Total frames: {stats.get('total_frames', 'N/A')}")
        print(f"   Processed frames: {stats.get('processed_frames', 'N/A')}")
        print(f"   Detection rate: {stats.get('detection_rate', 0):.1f}%")
        print(f"   Avg keypoints detected: {stats.get('avg_keypoints', 0):.1f}")
    
    # Download result
    print(f"\n4️⃣  Downloading result to: {output_video}")
    success = client.download_result(job_id, output_video)
    
    if success:
        file_size = Path(output_video).stat().st_size / (1024 * 1024)  # MB
        print(f"✅ Result downloaded successfully ({file_size:.2f} MB)")
        print(f"\n🎉 Done! You can now view the analyzed video at: {output_video}")
    else:
        print("❌ Failed to download result")
        sys.exit(1)


if __name__ == "__main__":
    main()
