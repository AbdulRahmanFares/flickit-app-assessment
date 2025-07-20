from src.video_io import VideoIO
from src.detection import Detector
from src.pose import PoseEstimator
from src.touch_counter import TouchCounter
from src.ball_spin import BallSpinEstimator
from src.velocity import VelocityCalculator
from src.overlay import Overlay
import cv2

INPUT_VIDEO = 'assessment_video.mp4'
OUTPUT_VIDEO = 'output_annotated.mp4'


def main():
    video = VideoIO(INPUT_VIDEO, OUTPUT_VIDEO)
    detector = Detector()
    pose_estimator = PoseEstimator()
    touch_counter = TouchCounter()
    ball_spin = BallSpinEstimator()
    velocity_calc = VelocityCalculator(video.fps)

    frame_idx = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_idx += 1
        detections = detector.detect(frame)
        ball_center = None
        ball_bbox = None
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            if det['cls'] == 32:  # Ball
                ball_center = ((x1 + x2) // 2, (y1 + y2) // 2)
                ball_bbox = (x1, y1, x2, y2)
            color = (0, 255, 0) if det['cls'] == 0 else (0, 0, 255)
            label = 'Player' if det['cls'] == 0 else 'Ball'
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        # Ball spin estimation
        rotation_text = ''
        if ball_bbox is not None:
            x1, y1, x2, y2 = ball_bbox
            curr_ball_crop = frame[y1:y2, x1:x2]
            rotation_text = ball_spin.estimate(curr_ball_crop)
        # Pose estimation
        keypoints = pose_estimator.get_keypoints(frame)
        right_foot = left_foot = player_pos = None
        if keypoints:
            pose_estimator.draw_leg_keypoints(frame, keypoints)
            h, w, _ = frame.shape
            if keypoints[32].visibility > 0.5:
                right_foot = (int(keypoints[32].x * w), int(keypoints[32].y * h))
            if keypoints[31].visibility > 0.5:
                left_foot = (int(keypoints[31].x * w), int(keypoints[31].y * h))
            if keypoints[23].visibility > 0.5 and keypoints[24].visibility > 0.5:
                x = int((keypoints[23].x + keypoints[24].x) / 2 * w)
                y = int((keypoints[23].y + keypoints[24].y) / 2 * h)
                player_pos = (x, y)
        # Touch detection and velocity
        new_touch, right_leg_touches, left_leg_touches = touch_counter.detect_and_count(ball_center, right_foot, left_foot)
        velocity = velocity_calc.update(player_pos, frame_idx, new_touch)
        # Overlay
        Overlay.draw_counts(frame, left_leg_touches, right_leg_touches, rotation_text, velocity)
        video.write(frame)
        cv2.imshow('Video Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
