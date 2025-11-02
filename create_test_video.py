"""
Create a simple test video with animated stick figure for testing
"""

import cv2
import numpy as np
import math

def create_test_dance_video(output_path='test_dance.mp4', duration=3, fps=30):
    """Create a test video with animated stick figure"""
    
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    for frame_num in range(total_frames):
        # Create black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Animation parameters
        t = frame_num / fps
        center_x = width // 2
        
        # Animate vertical movement (bobbing)
        bob = int(20 * math.sin(t * 2 * math.pi))
        head_y = 100 + bob
        
        # Animate arm swinging
        arm_angle = math.sin(t * 4 * math.pi) * 30
        
        # Draw stick figure
        # Head
        cv2.circle(frame, (center_x, head_y), 30, (255, 255, 255), -1)
        
        # Body
        body_start = (center_x, head_y + 30)
        body_end = (center_x, head_y + 150)
        cv2.line(frame, body_start, body_end, (255, 255, 255), 8)
        
        # Arms (animated)
        shoulder_y = head_y + 60
        left_arm_end = (
            int(center_x - 70 + arm_angle),
            int(shoulder_y + 60 - abs(arm_angle) * 0.5)
        )
        right_arm_end = (
            int(center_x + 70 - arm_angle),
            int(shoulder_y + 60 - abs(arm_angle) * 0.5)
        )
        cv2.line(frame, (center_x, shoulder_y), left_arm_end, (255, 255, 255), 8)
        cv2.line(frame, (center_x, shoulder_y), right_arm_end, (255, 255, 255), 8)
        
        # Legs (animated - alternating)
        leg_angle = math.sin(t * 4 * math.pi) * 20
        hip_y = head_y + 150
        left_leg_end = (
            int(center_x - 40 + leg_angle),
            hip_y + 120
        )
        right_leg_end = (
            int(center_x + 40 - leg_angle),
            hip_y + 120
        )
        cv2.line(frame, (center_x, hip_y), left_leg_end, (255, 255, 255), 8)
        cv2.line(frame, (center_x, hip_y), right_leg_end, (255, 255, 255), 8)
        
        # Add text
        cv2.putText(
            frame,
            f"Test Dance Video - Frame {frame_num + 1}/{total_frames}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )
        
        out.write(frame)
    
    out.release()
    print(f"✅ Test video created: {output_path}")
    print(f"   Duration: {duration}s, FPS: {fps}, Frames: {total_frames}")

if __name__ == "__main__":
    create_test_dance_video()
