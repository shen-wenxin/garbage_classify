from __future__ import print_function, division

import torch
from PIL import Image
from torch.autograd import Variable
from torchvision import datasets, transforms
import os


data_transforms = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


def get_key(dct, value):
    return [k for (k, v) in dct.items() if v == value]


if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # find the mapping of folder-to-label
    data = datasets.ImageFolder('data/train')
    mapping = data.class_to_idx
    # print(mapping)
    print("label mapping:")
    print(mapping)
    print("---------------------")
    # start testing
    net_name = 'efficientnet-b4'
    img_dir = 'data/train/3/fimg_521.jpg'

    # load model
    save_dir = 'data/model'
    # modelft_file = save_dir + "/" + net_name + '.pth'

    modelft_file = "data/model_for_each/net_005.pth"
    # load image
    img = Image.open(img_dir)
    inputs = data_transforms(img)
    inputs.unsqueeze_(0)

    # use GPU
    model = torch.load(modelft_file).cuda()
    model.eval()
    # use GPU
    inputs = Variable(inputs.cuda())

    # forward
    outputs = model(inputs)
    _, preds = torch.max(outputs.data, 1)

    class_name = get_key(mapping, preds.item())
    # use the mapping

    print(img_dir)
    print('prediction_label:', class_name)
    print(30*'--')
