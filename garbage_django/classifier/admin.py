from django.contrib import admin
from . import models
@admin.register(models.classifier)
class FileInfoAdmin(admin.ModelAdmin):
    list_display=('name','headimg')
    actions_on_top=True
    search_fields=['name']
