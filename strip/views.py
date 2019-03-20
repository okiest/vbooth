from django.shortcuts import render

# Create your views here.


from strip.models import *

def booth(request):
    context = {
    }
    return render(request, "booth.html", context)

