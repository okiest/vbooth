from django.shortcuts import render

# Create your views here.


from strip.models import *

def booth(request):
    context = {
    }
    return render(request, "booth.html", context)

def view_strip(request, strip_code):
    strip = PhotoStrip.objects.get(strip_code=strip_code)
    photos = Photo.objects.filter(photo_strip=strip)
    context = {
        "strip": strip,
        "photos": photos,
    }
    return render(request, "view_strip.html", context)

