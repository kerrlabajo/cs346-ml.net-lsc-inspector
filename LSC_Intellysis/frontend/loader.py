from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO("../runs/detect/train3/weights/best.pt")
model.predict(source="../test/Test1.png", show=True, conf=0.5)