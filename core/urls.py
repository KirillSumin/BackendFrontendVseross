from django.urls import path, register_converter
from . import views


app_name = 'core'
urlpatterns = [
    path('video', views.index),
]
