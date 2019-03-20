from django.conf.urls import url, include
from django.urls import path

from strip.views import *

urlpatterns = [
    path('', booth, name='booth')
]
