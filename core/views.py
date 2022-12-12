from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views import View
from django.http import HttpResponse, HttpRequest
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .models import History, Result
from .serializers import ResultSerializer
from django.shortcuts import render


def createSmthng(request):
    if request.POST:
      if "video" in request.FILES:
        video = request.FILES["video"]
      else:
        video = None
      # ...
      # Post.objects.create(...,file=video)
    #return redirect("feed")


def index(request):
  return render(request, "template.html", {'media': 'sample.mp4'})


# @api_view(['GET', 'POST'])
# def get_video_file(request):
#     """
#     doca for poluchenie and otpravka video
#     """
#
#     if request.method == 'GET':
#         video = request.FILES["video"]
#         return Response(video)
#
#     elif request.method == 'POST':
#         serializer = ResultSerializer(data=request.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# video_name = 'video.webm'
# with open(video_name, 'rb') as f:
#     video_content = f.read()
#
# story = History()
# story.video.save(video_name, ContentFile(video_content))
# story.save()
#
# resVideo_name = 'resVideo.webm'
# with open(resVideo_name, 'rb') as f:
#     resVideo_content = f.read()
#
# result = Result()
# result.inputData = story
# result.resVideo.save(resVideo_name, ContentFile(resVideo_content))
# result.save()