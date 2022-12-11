from django.contrib.auth.views import LogoutView
from django.urls import path

from dashboard.views import HistoryOfPassesView, livefe, TableWithEntrancesView, GetUserPhotoView

app_name = 'dashboard'
urlpatterns = [
    path('history_of_passes/', HistoryOfPassesView.as_view(), name='history_of_passes'),
    path('table_with_entrances/', TableWithEntrancesView.as_view(), name='table_with_entrances'),
    path('get_user_photo/', GetUserPhotoView.as_view(), name='get_user_photo'),
    path('livefe/', livefe, name='livefe')
]
