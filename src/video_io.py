import cv2

class VideoIO:
    def __init__(self, input_path, output_path=None):
        self.cap = cv2.VideoCapture(input_path)
        if not self.cap.isOpened():
            raise IOError(f'Cannot open video {input_path}')
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

    def read(self):
        return self.cap.read()

    def write(self, frame):
        if self.writer:
            self.writer.write(frame)

    def release(self):
        self.cap.release()
        if self.writer:
            self.writer.release()
