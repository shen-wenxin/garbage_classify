from django.shortcuts import render

from .models import classifier
from .forms import AddForm
from . import configs
from .predict import predictor
import os
import shutil
# Create your views here.
def classify(request):
    # 判断是否为 post 方法提交 
    if request.method == "POST":
        af = AddForm(request.POST, request.FILES)
        # 判断表单值是否和法
        if af.is_valid():
            classifier.objects.all().delete()
            shutil.rmtree(configs.MEDIA_IMG_PATH)
            os.mkdir(configs.MEDIA_IMG_PATH)
            img = af.cleaned_data['headimg']
            name = img.name
            file_type = name.split('.')[-1]
            if file_type != "jpg" and file_type != "png":
                message = configs.IMG_TYPE_ERROR
                return render(request, 'classifier/classify_upload.html',locals()) 

            new_img = classifier.objects.create(
                name=name,
                headimg=img
            )
            message = "上传成功"
            
            new_img.save()
            file_path = os.path.join(configs.MEDIA_IMG_PATH,name)
            # 得到结果之后可以将本地文件
            label = configs.LABEL_MAP[predictor.predict(file_path)[0]]
            
            
            message = "您的图片的分类结果为：{}".format(label)

            return render(request, 'classifier/classify_result.html',locals()) 
    else:
        af = AddForm()
        return render(request, 'classifier/classify_upload.html', locals())
