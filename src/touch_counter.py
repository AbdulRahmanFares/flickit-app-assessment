import math

class TouchCounter:
    def __init__(self, threshold=50):
        self.right_leg_touches = 0
        self.left_leg_touches = 0
        self.prev_right_touch = False
        self.prev_left_touch = False
        self.threshold = threshold

    @staticmethod
    def euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def detect_and_count(self, ball_center, right_foot, left_foot):
        right_touch = False
        left_touch = False
        if ball_center:
            if right_foot and self.euclidean_distance(ball_center, right_foot) < self.threshold:
                right_touch = True
            if left_foot and self.euclidean_distance(ball_center, left_foot) < self.threshold:
                left_touch = True
        new_touch = False
        if right_touch and not self.prev_right_touch:
            self.right_leg_touches += 1
            new_touch = True
        if left_touch and not self.prev_left_touch:
            self.left_leg_touches += 1
            new_touch = True
        self.prev_right_touch = right_touch
        self.prev_left_touch = left_touch
        return new_touch, self.right_leg_touches, self.left_leg_touches
