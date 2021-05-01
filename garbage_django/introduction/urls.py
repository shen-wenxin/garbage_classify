
from django.urls import path
from . import views

app_name = 'introduction'
urlpatterns = [
    path('', views.introduct, name='intro'),
    path('dataset/', views.dataset_intro),
    path('model/', views.model),
    path('finetune/', views.finetune),
    path('result/', views.result),
    path('reference/', views.reference),
    path('web_intro/', views.web_intro),
]