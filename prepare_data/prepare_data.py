# -*- coding: utf-8 -*-
"""
数据集准备脚本
"""
import os
import codecs
import shutil
try:
    import moxing as mox
except:
    print('not use moxing')
from glob import glob
from sklearn.model_selection import StratifiedShuffleSplit


def prepare_data_on_modelarts(args):
    """
    如果数据集存储在OBS，则需要将OBS上的数据拷贝到 ModelArts 中
    """
    # Create some local cache directories used for transfer data between local path and OBS path
    if not args.data_url.startswith('s3://'):
        args.data_local = args.data_url
    else:
        args.data_local = os.path.join(args.local_data_root, 'train_val')
        if not os.path.exists(args.data_local):
            mox.file.copy_parallel(args.data_url, args.data_local)
        else:
            print('args.data_local: %s is already exist, skip copy' % args.data_local)

    if not args.train_url.startswith('s3://'):
        args.train_local = args.train_url
    else:
        args.train_local = os.path.join(args.local_data_root, 'model_snapshots')
        if not os.path.exists(args.train_local):
            os.mkdir(args.train_local)

    if not args.test_data_url.startswith('s3://'):
        args.test_data_local = args.test_data_url
    else:
        args.test_data_local = os.path.join(args.local_data_root, 'test_data/')
        if not os.path.exists(args.test_data_local):
            mox.file.copy_parallel(args.test_data_url, args.test_data_local)
        else:
            print('args.test_data_local: %s is already exist, skip copy' % args.test_data_local)

    args.tmp = os.path.join(args.local_data_root, 'tmp')
    if not os.path.exists(args.tmp):
        os.mkdir(args.tmp)

    return args


def split_train_val(input_dir, output_train_dir, output_val_dir):
    """
    大赛发布的公开数据集是所有图片和标签txt都在一个目录中的格式
    如果需要使用 torch.utils.data.DataLoader 来加载数据，则需要将数据的存储格式做如下改变：
    1）划分训练集和验证集，分别存放为 train 和 val 目录；
    2）train 和 val 目录下有按类别存放的子目录，子目录中都是同一个类的图片
    本函数就是实现如上功能，建议先在自己的机器上运行本函数，然后将处理好的数据上传到OBS
    """
    if not os.path.exists(input_dir):
        print(input_dir, 'is not exist')
        return

    # 1. 检查图片和标签的一一对应
    label_file_paths = glob(os.path.join(input_dir, '*.txt'))
    valid_img_names = []
    valid_labels = []
    for file_path in label_file_paths:
        with codecs.open(file_path, 'r', 'utf-8') as f:
            line = f.readline()
        line_split = line.strip().split(', ')
        img_name = line_split[0]
        label_id = line_split[1]
        if os.path.exists(os.path.join(input_dir, img_name)):
            valid_img_names.append(img_name)
            valid_labels.append(int(label_id))
        else:
            print('error', img_name, 'is not exist')

    # 2. 使用 StratifiedShuffleSplit 划分训练集和验证集，可保证划分后各类别的占比保持一致
    # TODO，数据集划分方式可根据您的需要自行调整
    sss = StratifiedShuffleSplit(n_splits=1, test_size=500, random_state=0)
    sps = sss.split(valid_img_names, valid_labels)
    for sp in sps:
        train_index, val_index = sp

    label_id_name_dict = \
        {
            "0": "其他垃圾/一次性快餐盒",
            "1": "其他垃圾/污损塑料",
            "2": "其他垃圾/烟蒂",
            "3": "其他垃圾/牙签",
            "4": "其他垃圾/破碎花盆及碟碗",
            "5": "其他垃圾/竹筷",
            "6": "厨余垃圾/剩饭剩菜",
            "7": "厨余垃圾/大骨头",
            "8": "厨余垃圾/水果果皮",
            "9": "厨余垃圾/水果果肉",
            "10": "厨余垃圾/茶叶渣",
            "11": "厨余垃圾/菜叶菜根",
            "12": "厨余垃圾/蛋壳",
            "13": "厨余垃圾/鱼骨",
            "14": "可回收物/充电宝",
            "15": "可回收物/包",
            "16": "可回收物/化妆品瓶",
            "17": "可回收物/塑料玩具",
            "18": "可回收物/塑料碗盆",
            "19": "可回收物/塑料衣架",
            "20": "可回收物/快递纸袋",
            "21": "可回收物/插头电线",
            "22": "可回收物/旧衣服",
            "23": "可回收物/易拉罐",
            "24": "可回收物/枕头",
            "25": "可回收物/毛绒玩具",
            "26": "可回收物/洗发水瓶",
            "27": "可回收物/玻璃杯",
            "28": "可回收物/皮鞋",
            "29": "可回收物/砧板",
            "30": "可回收物/纸板箱",
            "31": "可回收物/调料瓶",
            "32": "可回收物/酒瓶",
            "33": "可回收物/金属食品罐",
            "34": "可回收物/锅",
            "35": "可回收物/食用油桶",
            "36": "可回收物/饮料瓶",
            "37": "有害垃圾/干电池",
            "38": "有害垃圾/软膏",
            "39": "有害垃圾/过期药物"
        }

    # 3. 创建 output_train_dir 目录下的所有标签名子目录
    for id in label_id_name_dict.keys():
        if not os.path.exists(os.path.join(output_train_dir, id)):
            os.mkdir(os.path.join(output_train_dir, id))

    # 4. 将训练集图片拷贝到 output_train_dir 目录
    for index in train_index:
        file_path = label_file_paths[index]
        with codecs.open(file_path, 'r', 'utf-8') as f:
            gt_label = f.readline()
        img_name = gt_label.split(',')[0].strip()
        id = gt_label.split(',')[1].strip()
        shutil.copy(os.path.join(input_dir, img_name), os.path.join(output_train_dir, id, img_name))

    # 5. 创建 output_val_dir 目录下的所有标签名子目录
    for id in label_id_name_dict.keys():
        if not os.path.exists(os.path.join(output_val_dir, id)):
            os.mkdir(os.path.join(output_val_dir, id))

    # 6. 将验证集图片拷贝到 output_val_dir 目录
    for index in val_index:
        file_path = label_file_paths[index]
        with codecs.open(file_path, 'r', 'utf-8') as f:
            gt_label = f.readline()
        img_name = gt_label.split(',')[0].strip()
        id = gt_label.split(',')[1].strip()
        shutil.copy(os.path.join(input_dir, img_name), os.path.join(output_val_dir, id, img_name))

    print('total samples: %d, train samples: %d, val samples:%d'
          % (len(valid_labels), len(train_index), len(val_index)))
    print('end')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='data prepare')
    parser.add_argument('--input_dir', required=True, type=str, help='input data dir')
    parser.add_argument('--output_train_dir', required=True, type=str, help='output train data dir')
    parser.add_argument('--output_val_dir', required=True, type=str, help='output validation data dir')
    args = parser.parse_args()
    if args.input_dir == '' or args.output_train_dir == '' or args.output_val_dir == '':
        raise Exception('You must specify valid arguments')
    if not os.path.exists(args.output_train_dir):
        os.makedirs(args.output_train_dir)
    if not os.path.exists(args.output_val_dir):
        os.makedirs(args.output_val_dir)
    split_train_val(args.input_dir, args.output_train_dir, args.output_val_dir)

