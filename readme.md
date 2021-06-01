# 垃圾分类网站

哈工大(深圳)软B 张正老师项目组 
[gitee](https://gitee.com/shen_wenxin0510/garbage_classify)/[github](https://github.com/shen-wenxin/garbage_classicy)

## 效果展示

### 首页

![首页](https://gitee.com/shen_wenxin0510/readme-pictures/raw/master/image-20210502175017215.png)


### 介绍界面
![介绍界面](https://gitee.com/shen_wenxin0510/readme-pictures/raw/master/image-20210502175254713.png)
### 分类界面

![分类上传](https://gitee.com/shen_wenxin0510/readme-pictures/raw/master/image-20210502175901239.png)
![分类结果](https://gitee.com/shen_wenxin0510/readme-pictures/raw/master/image-20210502175940404.png)

## 项目概述

​	改项目主要分为``图片分类算法/简单web框架``两部分。

​	项目文件夹结果如图

```
garbage_classify
	|--efficientNet	# 算法部分
	|--garbage_django	# django搭建的web框架
```

## 使用说明

### 环境要求

1、``python>=3.6``

2、``pytorch>=1.2.0``

3、``django>=3.2.0``

### efficientNet

#### 概述

​	该部分主要为该项目的算法部分。

```python
efficientNet
	|--data
		|--model	#存放efficientNet的best model
			|--efficientNet-b4.pth #该数据集下结果最好的网络
		|--test	
		|--train #数据集格式同Pytorch要求的格式
		|--val
	|--src
		|--train.py	# 微调之后的训练文件
		|--prepare_data.py	# 数据集准备文件
		|--test.py	# 测试文件
		|--test_prediction.py	#单张图片预测文件
	|--txt	# 训练日志
	|--efficientNet_pytorch.py	# 谷歌提供的efficientNet训练demo
	
```

#### 使用方法

##### 数据集准备 

​	若需要进行算法网络的训练，需按照**pytorch_efficientNet**数据集格式准备好数据集，放入``train/val/test``中。

​	pytorch数据集格式如下：

​	其中同一类的图片数据放到同一个文件夹中。

```
|--train #数据集格式同Pytorch要求的格式
	|--1
		|--xxx.jpg
		|--xxx.jpg
	|--2
		|--xxx.jpg
	...
```

​	该项目数据集太大，不一并上传，可通过[华为云官方](https://developer.huaweicloud.com/hero/forum.php?mod=viewthread&tid=24106)下载，还有[野生数据集](https://pan.baidu.com/s/1SulD2MqZx_U891JXeI2-2g)进行下载(提取码：epgs)。下载下来的数据集格式为华为云提供的数据集格式。文件格式如下：

```
|--train_data
	|--1.jpg
	|--1.txt
	...
```

​	其中``.txt``文件为同名`.jpg`的标签。

​	如果下载的是华为云提供的数据集格式，可利用``src/prepare_data.py``将其转为pytorch所需格式。

##### 训练

​	准备好数据集之后，命令行直接输入``python efficientNet_pytorch.py`` 即可进行训练。

​	``best_model``保存在``data/model``中。

##### 测试

​	训练完成后，视情况更改``src/test.py``中的模型路径`model_dir`和数据路径``data_dir``。

​	命令行输入``python src/test.py``即可。

##### 预测单张图片

​	视情况更改``src/test_prediction.py``中预测图片的路径`img_dir`跟模型所存的路径`modelft_file`

​	命令行输入``python src/test_prediction.py``即可。

### garbage_django 使用方法

#### 概述

```
garbage_django
	--classifier	#分类app
	--contact	#联系我app
	--garbage_django
	--home	#主页app
	--introduction	#介绍app
	--media
	--static
	--templates
	--manage.py
	--db.sqlite3
```

​	每个app中文件格式同django的app的文件格式

#### 使用方法

​	进入``garbage_django``目录文件下。

​	``python manage.py runserver 0.0.0.0:8000``可将其部署在局域网中。

​	之后浏览器访问``IP:8000``即可。端口号可自行更改。

##### 注意

​	在网页中，上传的待分类的图片文件名请不要包含``特殊字符``，不然可能会由于无法读取该图片信息而报错。

## 联系我

有问题请提``issue``.
