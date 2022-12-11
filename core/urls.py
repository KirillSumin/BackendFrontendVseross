from django.contrib.auth.views import LogoutView
from django.urls import path

from core.views import LoginView, TestView, FaceRecognizeView

app_name = 'core'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test/', TestView.as_view()),
    path('face_recognize/', FaceRecognizeView.as_view(), name='face_recognize'),
]
