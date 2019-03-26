try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
import base64
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile 


from strip.models import *


def single_stripper(strip_code, *args, **kwargs):
    photo_strip = PhotoStrip.objects.get(strip_code=strip_code)
    photos = Photo.objects.filter(photo_strip=photo_strip)
    im = Image.open(photos[0].strip_image.path)
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, format='JPEG')
    image_file = InMemoryUploadedFile(im_io, None, 'something.jpg', 'image/jpeg', im_io.__sizeof__(), None)
    photo_strip.strip_half.save("butthole.jpg", image_file)
    photo_strip.save()
 


