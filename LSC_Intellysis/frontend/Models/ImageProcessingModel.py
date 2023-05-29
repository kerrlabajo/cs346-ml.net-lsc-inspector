import torch
from ultralytics import YOLO  

class ImageProcessingModel:
  def __init__(self, model_path):
    self.model = YOLO(model_path)
    self.name = None
    self.extension = None
    self.result = None
    self.accuracy = None
    self.error_rate = None
    self.classification = None

  def analyze_image(self, file):
    self.result = self.model.predict(source=file, show=False, conf=0.20, save=True)
    path = self.result[0].path
    start_index = path.rfind("\\") + 1  # Find the last occurrence of "/" and add 1 to get the start index
    end_index = path.rfind(".")  # Find the index of the last occurrence of "."

    self.name = path[start_index:end_index]
    self.extension = path[end_index:]
    self.classification = torch.tensor(self.result[0].boxes.cls)
    self.accuracy = torch.tensor(self.result[0].boxes.conf) 
    self.error_rate = 1 - self.accuracy
    return self.result
  
  def getFile(self):
    self.accuracy = round(self.accuracy.item() * 100, 2)
    self.error_rate = round(self.error_rate.item() * 100, 2)
    self.classification = int(self.classification.item())
    return self.name, self.extension, self.accuracy, self.error_rate, self.classification
    