from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
# from two_factor.urls import urlpatterns as tf_urls
from django_otp.admin import OTPAdminSite


class OTPAdmin(OTPAdminSite):
    pass


from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'dadmin/', admin_site.urls),
    path(r'', include('core.urls', namespace='core')),
    # path('', include(tf_urls)),
]
