# 垃圾分类网站

哈工大(深圳)软B 张正老师项目组

## 效果展示

### 首页

![首页](https://github.com/shen-wenxin/readme_pic/blob/master/image-20210502175017215.png)

<img src="C:\Users\shen_\AppData\Roaming\Typora\typora-user-images\image-20210502175017215.png" alt="image-20210502175017215" style="zoom: 33%;" />

### 介绍界面

<img src="C:\Users\shen_\AppData\Roaming\Typora\typora-user-images\image-20210502175254713.png" alt="image-20210502175254713" style="zoom:33%;" />

### 分类界面

<img src="C:\Users\shen_\AppData\Roaming\Typora\typora-user-images\image-20210502175901239.png" alt="image-20210502175901239" style="zoom: 50%;" />![image-20210502175940404](C:\Users\shen_\AppData\Roaming\Typora\typora-user-images\image-20210502175940404.png)

<img src="C:\Users\shen_\AppData\Roaming\Typora\typora-user-images\image-20210502175940404.png" alt="image-20210502175940404" style="zoom:33%;" />

## 项目概述

​	改项目主要分为``图片分类算法/简单web框架``两部分。

​	项目文件夹结果如图

```
garbage_classify
	--efficientNet	# 算法部分
	--garbage_django	# django搭建的web框架
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
	--data
		--model	#存放efficientNet的best model
			--efficientNet-b4.pth #该数据集下结果最好的网络
		--test	
		--train #数据集格式同Pytorch要求的格式
		--val
	--src
		--train.py	# 微调之后的训练文件
		--prepare_data.py	# 数据集准备文件
		--test.py	# 测试文件
		--test_prediction.py	#单张图片预测文件
	--txt	# 训练日志
	--efficientNet_pytorch.py	# 谷歌提供的efficientNet训练demo
	
```

#### 使用方法

​	若需要进行算法网络的训练，需按照**pytorch_efficientNet**数据集格式准备好数据集，放入``train/val/test``中。

​	数据集格式如下：

```
--train #数据集格式同Pytorch要求的格式
	--1
		--xxx.jpg
		--xxx.jpg
	--2
		--xxx.jpg
	...
```

​	该项目数据集太大，不一并上传，可通过[华为云官方](https://developer.huaweicloud.com/hero/forum.php?mod=viewthread&tid=24106)下载，还有[野生数据集](https://pan.baidu.com/s/1SulD2MqZx_U891JXeI2-2g)进行下载(提取码：epgs)。

​	如果下载的是华为云提供的数据集格式，可利用``src/prepare_data.py``将其转为所需格式。

​	准备好数据集之后，命令行直接输入``python efficientNet_pytorch.py`` 即可进行训练。

​	``best_model``保存在``data/model``中。

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

​	之后浏览器访问``IP:8000``即可。

## 联系我

有问题请提``issue``.
