import cv2

class Overlay:
    @staticmethod
    def draw_counts(frame, left_leg_touches, right_leg_touches, rotation_text, velocity):
        font_scale = 0.6
        thickness = 2
        y0 = 30
        dy = 25
        cv2.putText(frame, f'Left Leg Touches: {left_leg_touches}', (20, y0), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 255), thickness)
        cv2.putText(frame, f'Right Leg Touches: {right_leg_touches}', (20, y0 + dy), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)
        cv2.putText(frame, f'Ball Direction: {rotation_text}', (20, y0 + 2 * dy), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)
        cv2.putText(frame, f'Player Velocity: {velocity:.1f} px/s', (20, y0 + 3 * dy), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 128, 255), thickness)
