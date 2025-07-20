from ultralytics import YOLO

class Detector:
    def __init__(self, model_path='models/yolo11n.pt'):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            detections.append({'bbox': (x1, y1, x2, y2), 'cls': cls, 'conf': conf})
        return detections
