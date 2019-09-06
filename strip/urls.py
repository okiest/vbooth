from django.conf.urls import url, include
from django.urls import path

from strip.views import *
from strip.models import *

urlpatterns = [
    path('', booth, name='booth'),
    path('lobby/<strip_code>', lobby, name='lobby'),
    path('printed/<strip_code>', printed_strip, name='printed-strip'),
    path('postcard/', postcard, name='postcard'),
    path('postcard/lobby/<strip_code>', postcard_lobby, name='postcard-lobby'),
    path('kiosk/', kiosk, name='kiosk'),
    path('kiosk/lobby/<strip_code>', kiosk_lobby, name='kiosk-lobby'),
    path('connected/', connected, name='connected'),
]
