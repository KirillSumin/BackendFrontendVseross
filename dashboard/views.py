import threading

import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
from django.views.generic import ListView, TemplateView
from vidgear.gears import NetGear

from core.models import EntranceHistory


class HistoryOfPassesView(ListView):
    template_name = 'history_of_passes.html'
    model = EntranceHistory


class TableWithEntrancesView(ListView):
    template_name = 'table_with_entrances.html'
    model = EntranceHistory

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-entry_date')[:20]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = []
        for entrance in context['object_list']:
            exit_date = entrance.exit_date
            if not exit_date:
                exit_date = 'На территории'
            if entrance.auth_type == 'auto':
                auth_type = 'Номерной знак'
            elif entrance.auth_type == 'face':
                auth_type = 'Распознование лица'
            obj = {'entrance': entrance, 'exit_date': exit_date, 'auth_type': auth_type}
            object_list.append(obj)
        context['object_list'] = object_list

        # context['last_entrance_photo_url'] = object_list[0]['entrance'].user.user_photo.url
        return context


class GetUserPhotoView(ListView):
    template_name = 'get_user_photo.html'
    model = EntranceHistory

    def get_queryset(self):
        queryset = self.model.objects.all()[:5]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_entry = self.model.objects.all().order_by('-entry_date')[0]
        if last_entry.auth_type == 'auto':
            context['last_entrance_photo_url'] = None
        else:
            context['last_entrance_photo_url'] = last_entry.user.user_photo.url
        return context

client = NetGear(
    address="127.0.0.1",  # don't change this
    port="5455",
    pattern=2,
    receive_mode=True,
    logging=True,
)

class VideoCamera(object):
    def __init__(self):
        # CAMERA_IP_PORT = 'http://192.168.0.111:4747/video'
        # self.video = cv2.VideoCapture(0)
        self.frame = client.recv()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        client.close()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.frame = client.recv()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass