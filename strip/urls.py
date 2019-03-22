from django.conf.urls import url, include
from django.urls import path

from strip.views import *
from strip.models import *

urlpatterns = [
    path('', booth, name='booth'),
    path('view/<strip_code>', view_strip, name='view-strip'),
]
