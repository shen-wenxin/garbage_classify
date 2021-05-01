# -*- coding: utf-8 -*-
from torchvision import datasets, transforms
import torch
from torch import nn
import torch.optim as optim
import argparse
import warnings
import torch.optim.lr_scheduler as lr_scheduler
from torch.utils.data.dataloader import default_collate  # 导入默认的拼接方式
from efficientnet_pytorch import EfficientNet
from label_smooth import LabelSmoothSoftmaxCE
import os
from PIL import Image
"""test file"""
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'

#   to the ImageFolder structure
data_dir = "./data/"

model_dir = "./data/model/efficientnet-b4.pth"
# load module

input_size = 380
batch_size = 20  # 批处理尺寸(batch_size)

type="val"

def my_collate_fn(batch):
    '''
    batch中每个元素形如(data, label)
    '''
    # 过滤为None的数据
    batch = list(filter(lambda x: x[0] is not None, batch))
    if len(batch) == 0: return torch.Tensor()
    return default_collate(batch)  # 用默认方式拼接过滤后的batch数据

def pridict():
    net = torch.load(model_dir)

    # Detect if we have a GPU available
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    net.to(device)

    # 预测
    net.eval()
    data_transforms = {
        type: transforms.Compose([
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
    }
    # Create test dataset
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in [type]}
    # Create training and validation dataloaders
    dataloaders_dict = {
        x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=12,
                                       collate_fn=my_collate_fn) for x in [type]}
    with torch.no_grad():
        correct = 0
        total = 0
        for data in dataloaders_dict[type]:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = net(images)
            # 取得分最高的那个类 (outputs.data的索引号)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).cpu().sum()
        print('测试分类准确率为：%.3f%%' % (100. * float(correct) / float(total)))


pridict()