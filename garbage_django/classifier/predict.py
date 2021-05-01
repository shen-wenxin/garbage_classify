from __future__ import print_function, division

import torch
from PIL import Image
from torch.autograd import Variable
from torchvision import datasets, transforms
import os

class ImgPrediction:
    def __init__(self):
        self.data_transforms = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        self.mapping = {'0': 0, '1': 1, '10': 2, '11': 3, '12': 4, 
                        '13': 5, '14': 6, '15': 7, '16': 8, '17': 9, 
                        '18': 10, '19': 11, '2': 12, '20': 13, '21': 14, 
                        '22': 15, '23': 16, '24': 17, '25': 18, '26': 19, 
                        '27': 20, '28': 21, '29': 22, '3': 23, '30': 24, 
                        '31': 25, '32': 26, '33': 27, '34': 28, '35': 29, 
                        '36': 30, '37': 31, '38': 32, '39': 33, '4': 34, 
                        '5': 35, '6': 36, '7': 37, '8': 38, '9': 39}
        self.net_name = 'efficientnet-b4'
        self.modelft_file = "classifier/efficientNet-b4.pth"
        self.model = torch.load(self.modelft_file,map_location='cpu')
        self.model.eval()

    def get_key(self, dct, value):
        return [k for (k, v) in dct.items() if v == value]

    def predict(self,img_dir):
        img = Image.open(img_dir)
        inputs = self.data_transforms(img)
        inputs.unsqueeze_(0)
        inputs = Variable(inputs)
        outputs = self.model(inputs)
        _, preds = torch.max(outputs.data, 1)
        class_name = self.get_key(self.mapping, preds.item())
        return class_name

predictor = ImgPrediction()



# if __name__ == "__main__":

#     img_dir = 'media/img/harmful_38_1.jpg'
#     predictor = ImgPrediction()
#     print(predictor.predict(img_dir))
    