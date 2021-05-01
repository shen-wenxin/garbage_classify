# classifier/urls.py
from django.urls import path
from . import views

app_name = 'classifier'
urlpatterns = [
    path('', views.classify, name='add'),
]