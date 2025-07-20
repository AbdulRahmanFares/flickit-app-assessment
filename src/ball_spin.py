import cv2
import numpy as np

class BallSpinEstimator:
    def __init__(self):
        self.prev_ball_crop = None

    def extract_optical_flow_features(self, prev_ball_crop, curr_ball_crop):
        prev_gray = cv2.cvtColor(prev_ball_crop, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_ball_crop, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mean_flow_y = np.mean(flow[..., 1])
        std_flow_y = np.std(flow[..., 1])
        mean_flow_x = np.mean(flow[..., 0])
        std_flow_x = np.std(flow[..., 0])
        return {
            'mean_flow_y': mean_flow_y,
            'std_flow_y': std_flow_y,
            'mean_flow_x': mean_flow_x,
            'std_flow_x': std_flow_x
        }

    def spin_rule_classifier(self, features):
        if features['mean_flow_y'] < -1 and features['std_flow_y'] > 0.5:
            return 'Backspin'
        elif features['mean_flow_y'] > 1 and features['std_flow_y'] > 0.5:
            return 'Forward Spin'
        else:
            return 'No Spin'

    def estimate(self, curr_ball_crop):
        rotation_text = ''
        if self.prev_ball_crop is not None and curr_ball_crop is not None and curr_ball_crop.shape == self.prev_ball_crop.shape and curr_ball_crop.size > 0:
            features = self.extract_optical_flow_features(self.prev_ball_crop, curr_ball_crop)
            rotation_text = self.spin_rule_classifier(features)
        self.prev_ball_crop = curr_ball_crop.copy() if curr_ball_crop is not None and curr_ball_crop.size > 0 else None
        return rotation_text
