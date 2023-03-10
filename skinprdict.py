# -*- coding: utf-8 -*-
"""Predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y8AQFaTu0IbmcGvKMORh_wa7c6hHeRn_
"""

import sklearn
sklearn.__version__





import torchvision
import torch
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as T
import numpy as np
from sklearn.preprocessing import LabelEncoder
import torch.nn as nn
from torchvision.models import vgg16
from sklearn.model_selection import train_test_split
import torch.nn.functional as Fun
import cv2

device = 'cuda' if torch.cuda.is_available() else 'cpu'

transforms = T.Compose(
        [T.ToTensor(),
        T.Normalize(mean=[0.485,
           0.456, 0.406],std=[0.229, 0.224, 0.225])]
        )

    
def read_transform(img):
        f = img
        im = cv2.imread(f)
        im = cv2.resize(im, (224,224))
        im = transforms(im)
        return torch.tensor(im,dtype=torch.float).to(device)

import torch
import torch.nn as nn
import torchvision

def get_model():
    class NeuralNetwork(nn.Module):
        def __init__(self):
          super(NeuralNetwork, self).__init__()
          self.model = torchvision.models.vgg16(pretrained=True)
          for param in self.model.features.parameters():
                        param.requires_grad = False


          self.numeric_features_ = nn.Sequential(
              nn.Linear(3,64),
              nn.ReLU(inplace=True),
              nn.Dropout(),
          )
          
          self.combined_ = nn.Sequential(
              nn.Linear(64 + 1000, 512),
              nn.ReLU(inplace=True),
              nn.Dropout(),
              nn.Linear(512, 128),
              nn.ReLU(inplace=True),
              nn.Dropout(),
              nn.Linear(128, 7),
              nn.Softmax()
          )

        def forward(self, input1, age):
          image_features = self.model(input1)
          numerical_features = self.numeric_features_(torch.tensor((age)))
          # numerical_features = numerical_features.view(numerical_features.size(0), -1)
          combined_features = torch.hstack((image_features, numerical_features.reshape(-1,64)))
          return self.combined_(combined_features)

          
    model = NeuralNetwork()
    model = model.to(device)
    return model
def load_model(model_path):
  model = get_model()
  state_dict = torch.load(model_path)
  return model,state_dict



def predict(image, sex, location,age):
  img = read_transform(image)
  img = img.to(device)
  tabular = [sex, location, age]
  tabular = torch.Tensor(tabular).to(torch.float)
  model, state_dict = load_model('model.path')
  model.load_state_dict(state_dict)
  output = model(img.unsqueeze_(0), tabular.unsqueeze_(0))
  pred, conf = output.max(-1)
  return conf.item(), pred

predict('image_path', 'sex', 'location', 'age')