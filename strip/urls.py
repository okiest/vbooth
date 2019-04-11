from django.conf.urls import url, include
from django.urls import path

from strip.views import *
from strip.models import *

urlpatterns = [
    path('', booth, name='booth'),
    path('lobby/<strip_code>', lobby, name='lobby'),
    path('printed/<strip_code>', printed_strip, name='printed-strip'),
    path('download/<strip_code>', download_strip, name='download-strip'),
]
