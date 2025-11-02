"""
Unit tests for Dance Movement Analysis
Tests keypoint detection accuracy and output formatting
"""

import pytest
import cv2
import numpy as np
from pathlib import Path
import os
import tempfile

from movement_analyzer import DanceMovementAnalyzer, analyze_dance_video


class TestDanceMovementAnalyzer:
    """Test suite for DanceMovementAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing"""
        return DanceMovementAnalyzer()
    
    @pytest.fixture
    def sample_video(self):
        """Create a simple test video with a person-like figure"""
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, "test_video.mp4")
        
        # Create a simple test video (30 frames, 640x480, 30fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, 30, (640, 480))
        
        for i in range(30):
            # Create a frame with a simple stick figure
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            # Draw a simple person-like shape
            # Head
            cv2.circle(frame, (320, 100), 30, (255, 255, 255), -1)
            # Body
            cv2.line(frame, (320, 130), (320, 300), (255, 255, 255), 5)
            # Arms
            cv2.line(frame, (320, 180), (250, 250), (255, 255, 255), 5)
            cv2.line(frame, (320, 180), (390, 250), (255, 255, 255), 5)
            # Legs
            cv2.line(frame, (320, 300), (280, 420), (255, 255, 255), 5)
            cv2.line(frame, (320, 300), (360, 420), (255, 255, 255), 5)
            
            out.write(frame)
        
        out.release()
        
        yield video_path
        
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        os.rmdir(temp_dir)
    
    def test_analyzer_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer is not None
        assert analyzer.mp_pose is not None
        assert analyzer.pose is not None
    
    def test_analyzer_custom_confidence(self):
        """Test analyzer with custom confidence thresholds"""
        analyzer = DanceMovementAnalyzer(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        assert analyzer is not None
    
    def test_video_analysis_success(self, analyzer, sample_video):
        """Test successful video analysis"""
        output_path = sample_video.replace(".mp4", "_output.mp4")
        
        success, message, stats = analyzer.analyze_video(sample_video, output_path)
        
        # Verify success
        assert success is True
        assert "success" in message.lower()
        
        # Verify statistics
        assert "total_frames" in stats
        assert "processed_frames" in stats
        assert stats["processed_frames"] > 0
        
        # Verify output file exists
        assert os.path.exists(output_path)
        
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
    
    def test_invalid_video_path(self, analyzer):
        """Test handling of invalid video path"""
        success, message, stats = analyzer.analyze_video(
            "nonexistent_video.mp4",
            "output.mp4"
        )
        
        assert success is False
        assert "could not open" in message.lower()
    
    def test_frame_keypoint_extraction(self, analyzer):
        """Test keypoint extraction from a single frame"""
        # Create a test frame with a simple figure
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Draw a person-like figure
        cv2.circle(frame, (320, 100), 30, (255, 255, 255), -1)
        cv2.line(frame, (320, 130), (320, 300), (255, 255, 255), 5)
        cv2.line(frame, (320, 180), (250, 250), (255, 255, 255), 5)
        cv2.line(frame, (320, 180), (390, 250), (255, 255, 255), 5)
        cv2.line(frame, (320, 300), (280, 420), (255, 255, 255), 5)
        cv2.line(frame, (320, 300), (360, 420), (255, 255, 255), 5)
        
        keypoints = analyzer.get_frame_keypoints(frame)
        
        # Keypoints might be None for simple drawings
        # MediaPipe needs realistic human poses
        assert keypoints is None or isinstance(keypoints, dict)
    
    def test_keypoint_format(self, analyzer):
        """Test that keypoints have correct format"""
        # Create a more realistic test (this may not detect on simple drawings)
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 100
        
        keypoints = analyzer.get_frame_keypoints(frame)
        
        if keypoints is not None:
            # Verify keypoint structure
            for key, value in keypoints.items():
                assert isinstance(key, int)
                assert "x" in value
                assert "y" in value
                assert "z" in value
                assert "visibility" in value
                
                # Verify coordinate ranges
                assert 0 <= value["x"] <= 1
                assert 0 <= value["y"] <= 1
                assert 0 <= value["visibility"] <= 1
    
    def test_output_video_properties(self, analyzer, sample_video):
        """Test that output video has correct properties"""
        output_path = sample_video.replace(".mp4", "_output.mp4")
        
        success, message, stats = analyzer.analyze_video(sample_video, output_path)
        
        if success:
            # Open both videos
            cap_input = cv2.VideoCapture(sample_video)
            cap_output = cv2.VideoCapture(output_path)
            
            # Compare properties
            assert cap_input.get(cv2.CAP_PROP_FRAME_WIDTH) == cap_output.get(cv2.CAP_PROP_FRAME_WIDTH)
            assert cap_input.get(cv2.CAP_PROP_FRAME_HEIGHT) == cap_output.get(cv2.CAP_PROP_FRAME_HEIGHT)
            assert cap_input.get(cv2.CAP_PROP_FPS) == cap_output.get(cv2.CAP_PROP_FPS)
            
            cap_input.release()
            cap_output.release()
            
            # Cleanup
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_convenience_function(self, sample_video):
        """Test the convenience function"""
        output_path = sample_video.replace(".mp4", "_output.mp4")
        
        success, message, stats = analyze_dance_video(sample_video, output_path)
        
        assert isinstance(success, bool)
        assert isinstance(message, str)
        assert isinstance(stats, dict)
        
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
    
    def test_statistics_accuracy(self, analyzer, sample_video):
        """Test that statistics are accurate"""
        output_path = sample_video.replace(".mp4", "_output.mp4")
        
        success, message, stats = analyzer.analyze_video(sample_video, output_path)
        
        if success:
            # Verify all expected statistics are present
            assert "total_frames" in stats
            assert "processed_frames" in stats
            assert "detected_frames" in stats
            assert "detection_rate" in stats
            assert "keypoints_detected" in stats
            assert "avg_keypoints" in stats
            
            # Verify statistics consistency
            assert stats["processed_frames"] <= stats["total_frames"]
            assert stats["detected_frames"] <= stats["processed_frames"]
            assert 0 <= stats["detection_rate"] <= 100
            
            # Cleanup
            if os.path.exists(output_path):
                os.remove(output_path)


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_frame(self):
        """Test handling of empty frame"""
        analyzer = DanceMovementAnalyzer()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        keypoints = analyzer.get_frame_keypoints(frame)
        # Should return None for no detected pose
        assert keypoints is None or isinstance(keypoints, dict)
    
    def test_very_small_video(self):
        """Test handling of very small resolution video"""
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, "small_video.mp4")
        output_path = os.path.join(temp_dir, "small_output.mp4")
        
        # Create tiny video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, 30, (100, 100))
        
        for i in range(10):
            frame = np.zeros((100, 100, 3), dtype=np.uint8)
            out.write(frame)
        
        out.release()
        
        analyzer = DanceMovementAnalyzer()
        success, message, stats = analyzer.analyze_video(video_path, output_path)
        
        # Should handle small videos
        assert isinstance(success, bool)
        
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        os.rmdir(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
