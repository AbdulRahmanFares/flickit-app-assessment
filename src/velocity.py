import math

class VelocityCalculator:
    def __init__(self, fps):
        self.prev_player_pos = None
        self.prev_touch_frame_idx = 0
        self.last_velocity = 0.0
        self.fps = fps

    @staticmethod
    def euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def update(self, player_pos, frame_idx, new_touch):
        if new_touch and player_pos and self.prev_player_pos:
            dist = self.euclidean_distance(player_pos, self.prev_player_pos)
            frames_elapsed = frame_idx - self.prev_touch_frame_idx
            time_elapsed = frames_elapsed / self.fps if self.fps > 0 else 1.0
            self.last_velocity = dist / time_elapsed
            self.prev_touch_frame_idx = frame_idx
        if new_touch and player_pos:
            self.prev_player_pos = player_pos
        return self.last_velocity
