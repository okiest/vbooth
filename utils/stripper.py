import base64
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
from PIL import Image

from django.conf import settings
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile 


from strip.models import *


def single_stripper(strip_code, *args, **kwargs):
    photo_strip = PhotoStrip.objects.get(strip_code=strip_code)
    photos = Photo.objects.filter(photo_strip=photo_strip)
    #with open(photos[0].strip_image.path, 'rb') as f:
    #    print(dir(f))
    #    contents = base64.b64encode(f.read()).decode()
        #contents = f.read()
    #f = File(open(photos[0].strip_image.path, 'r'))
    #photos[0].strip_image.path
    #photo_strip.strip_half.save('', contents) 
    im = Image.open(photos[0].strip_image.path)
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, format='JPEG')
    image_file = InMemoryUploadedFile(im_io, None, 'something.jpg', 'image/jpeg', im_io.__sizeof__(), None)
    #im = ImageFile(im)
    #print(im.name)
    photo_strip.strip_half.save("butthole.jpg", image_file)
    photo_strip.save()
 

    #photo_strip.strip_half = photos[0].strip_image.path
    #photo_strip.save()



