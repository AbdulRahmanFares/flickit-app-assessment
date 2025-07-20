import mediapipe as mp
import cv2

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def get_keypoints(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)
        if results.pose_landmarks:
            return results.pose_landmarks.landmark
        return None

    def draw_leg_keypoints(self, frame, landmarks, visibility_th=0.5):
        h, w, _ = frame.shape
        right_leg = [24, 26, 28, 32]
        left_leg = [23, 25, 27, 31]
        for idx in right_leg:
            if landmarks[idx].visibility > visibility_th:
                cx, cy = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
                cv2.circle(frame, (cx, cy), 6, (255, 0, 0), -1)
        for idx in left_leg:
            if landmarks[idx].visibility > visibility_th:
                cx, cy = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
                cv2.circle(frame, (cx, cy), 6, (0, 255, 255), -1)
