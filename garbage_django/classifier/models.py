from django.db import models

# Create your models here.

class classifier(models.Model):
    name = models.CharField('文件名称',max_length=200, null = False)
    headimg = models.FileField(upload_to="img/")
    
    class Meta:
        db_table = "Img"
        verbose_name = "待分类图片"
        verbose_name_plural = verbose_name
        
    # 返回名称
    def __str__(self):
        return self.name