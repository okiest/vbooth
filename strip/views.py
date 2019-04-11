from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from utils.stripper import single_stripper, big_stripper

from strip.models import *

@login_required
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
    #if "print-strip" in request.POST:
    #    print("Redirecting to print page")
    #    return redirect("print/{}".format(strip_code)) 
    return render(request, "view_strip.html", context)

def print_strip(request, strip_code):
    strip = PhotoStrip.objects.get(strip_code=strip_code)
    if strip.strip_whole:
        pass
    else:
        big_stripper(strip_code)
    if strip.strip_half:
        pass
    else:
        single_stripper(strip_code)
    photos = Photo.objects.filter(photo_strip=strip)
    context = {
        "strip": strip,
        "photos": photos,
    }
    return render(request, "print_strip.html", context)

@login_required
def download_strip(request, strip_code):
    strip = PhotoStrip.objects.get(strip_code=strip_code)
    if strip.strip_whole:
        pass
    else:
        big_stripper(strip_code)
    if strip.strip_half:
        pass
    else:
        single_stripper(strip_code)
    photos = Photo.objects.filter(photo_strip=strip)
    context = {
        "strip": strip,
        "photos": photos,
    }
    return render(request, "download_strip.html", context)
