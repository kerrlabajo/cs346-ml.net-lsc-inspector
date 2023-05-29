import torch
from ultralytics import YOLO 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 

class ImageProcessingModel:
  def __init__(self, model_path):
    self.model = YOLO(model_path)
    # Initialize MongoDB
    uri = "mongodb+srv://rauljay:26A0x6Qlj5tlenvZ@lscdb.tmmh6on.mongodb.net/?retryWrites=true&w=majority"
    self.client = MongoClient(uri, server_api=ServerApi('1'))
    self.db = self.client['LSC_Inspector']
    self.collection = self.db["image_history"]
    self.name = None
    self.extension = None
    self.result = None
    self.accuracy = None
    self.error_rate = None  
    self.classification = None

  def analyze_image(self, file):
    self.result = self.model.predict(source=file, show=False, conf=0.20, save=True)
    self.classification = torch.tensor(self.result[0].boxes.cls)
    self.accuracy = torch.tensor(self.result[0].boxes.conf) 
    self.error_rate = 1 - self.accuracy
    path = self.result[0].path
    start_index = path.rfind("\\") + 1  # Find the last occurrence of "/" and add 1 to get the start index
    end_index = path.rfind(".")  # Find the index of the last occurrence of "."

    self.name = path[start_index:end_index]
    self.extension = path[end_index+1:]
    return self.result
  
  def insertIntoDB(self, data):
    self.collection.insert_one(data)

  def getFile(self):
    if isinstance(self.accuracy, float) and isinstance(self.error_rate, float) and isinstance(self.classification, int):
      return self.name, self.extension, self.accuracy, self.error_rate, self.classification
    else:
      self.accuracy = round(self.accuracy.item() * 100, 2)
      self.error_rate = round(self.error_rate.item() * 100, 2)
      self.classification = int(self.classification.item())
    return self.name, self.extension, self.accuracy, self.error_rate, self.classification
    