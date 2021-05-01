# HITSZ 2021 软B项目 垃圾分类网站

## 一、算法模块

### 1 数据集准备

利用网上开源的数据集作为训练集，近2w张

测试集数量：500

数据集格式：同pytorch_efficientNet要求的格式

```
-data
	-model
	-train
		-1
		-2
		…
	-val
		-1
		…
```

### 2训练参数

``batch_size = 64``

``lr = 0.01``

``momentum = 0.9``

``num_epochs=15``

``input_size=224``

``class_num=40``

| baseline        | 准确率  |
| --------------- | ------- |
| efficientnet-b4 | 96.774% |
|                 |         |
|                 |         |

