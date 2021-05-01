# classifier/forms.py
from django import forms

# 表单类用以生成表单
class AddForm(forms.Form):
    headimg = forms.FileField(label="",widget=forms.FileInput(attrs={'class': 'form-file text-center'}))