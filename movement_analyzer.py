"""
Dance Movement Analysis Module
Uses MediaPipe Pose to detect body keypoints and overlay skeleton on dance videos.
"""

import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DanceMovementAnalyzer:
    """
    Analyzes dance movements using MediaPipe Pose detection.
    Detects body keypoints and overlays skeleton visualization.
    """
    
    def __init__(self, 
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the analyzer with MediaPipe Pose.
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=2  # Use most accurate model
        )
        
        logger.info("DanceMovementAnalyzer initialized successfully")
    
    def analyze_video(self, 
                     input_path: str, 
                     output_path: str) -> Tuple[bool, str, dict]:
        """
        Analyze a dance video and create output with skeleton overlay.
        
        Args:
            input_path: Path to input video file
            output_path: Path to save output video
            
        Returns:
            Tuple of (success, message, statistics)
        """
        try:
            # Open input video
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                return False, f"Could not open video: {input_path}", {}
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Processing video: {width}x{height} @ {fps}fps, {total_frames} frames")
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Statistics tracking
            stats = {
                'total_frames': total_frames,
                'processed_frames': 0,
                'detected_frames': 0,
                'keypoints_detected': []
            }
            
            frame_count = 0
            
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break
                
                frame_count += 1
                
                # Convert BGR to RGB for MediaPipe
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_rgb.flags.writeable = False
                
                # Process the frame with MediaPipe Pose
                results = self.pose.process(image_rgb)
                
                # Convert back to BGR for OpenCV
                image_rgb.flags.writeable = True
                image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                
                # Draw pose landmarks if detected
                if results.pose_landmarks:
                    stats['detected_frames'] += 1
                    
                    # Draw the skeleton overlay
                    self.mp_drawing.draw_landmarks(
                        image_bgr,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                    )
                    
                    # Count visible keypoints
                    visible_keypoints = sum(
                        1 for landmark in results.pose_landmarks.landmark
                        if landmark.visibility > 0.5
                    )
                    stats['keypoints_detected'].append(visible_keypoints)
                
                # Add frame counter overlay
                cv2.putText(
                    image_bgr, 
                    f"Frame: {frame_count}/{total_frames}", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (0, 255, 0), 
                    2
                )
                
                # Write processed frame
                out.write(image_bgr)
                stats['processed_frames'] += 1
                
                # Log progress
                if frame_count % 30 == 0:
                    logger.info(f"Progress: {frame_count}/{total_frames} frames")
            
            # Cleanup
            cap.release()
            out.release()
            
            # Calculate final statistics
            stats['detection_rate'] = (
                stats['detected_frames'] / stats['processed_frames'] * 100
                if stats['processed_frames'] > 0 else 0
            )
            stats['avg_keypoints'] = (
                np.mean(stats['keypoints_detected'])
                if stats['keypoints_detected'] else 0
            )
            
            logger.info(f"Analysis complete: {stats['detection_rate']:.1f}% detection rate")
            
            return True, "Video processed successfully", stats
            
        except Exception as e:
            logger.error(f"Error analyzing video: {str(e)}")
            return False, f"Error: {str(e)}", {}
    
    def get_frame_keypoints(self, frame: np.ndarray) -> Optional[dict]:
        """
        Extract keypoints from a single frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Dictionary with keypoint coordinates or None if not detected
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # Process frame
        results = self.pose.process(image_rgb)
        
        if results.pose_landmarks:
            keypoints = {}
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                keypoints[idx] = {
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                }
            return keypoints
        
        return None
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'pose'):
            self.pose.close()


def analyze_dance_video(input_path: str, output_path: str) -> Tuple[bool, str, dict]:
    """
    Convenience function to analyze a dance video.
    
    Args:
        input_path: Path to input video
        output_path: Path to save output video
        
    Returns:
        Tuple of (success, message, statistics)
    """
    analyzer = DanceMovementAnalyzer()
    return analyzer.analyze_video(input_path, output_path)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python movement_analyzer.py <input_video> <output_video>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    success, message, stats = analyze_dance_video(input_file, output_file)
    
    if success:
        print(f"✓ {message}")
        print(f"  Processed: {stats['processed_frames']} frames")
        print(f"  Detection rate: {stats['detection_rate']:.1f}%")
        print(f"  Avg keypoints: {stats['avg_keypoints']:.1f}")
    else:
        print(f"✗ {message}")
        sys.exit(1)
