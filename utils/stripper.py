import datetime
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageChops

from django.core.files.uploadedfile import InMemoryUploadedFile 


from strip.models import *

def get_four_square():
    im1_pos = (60, 60, 1980, 1140)
    im2_pos = (2100, 60, 4020, 1140)
    im3_pos = (60, 1260, 1980, 2340)
    im4_pos = (2100, 1260, 4020, 2340)
    positions = [im1_pos, im2_pos, im3_pos, im4_pos]
    return positions

def get_coorder(orientation):
    print(orientation)
    if orientation == 'H':
        im1_pos = (40, 60, 1320, 780)
        im2_pos = (40, 840, 1320, 1560)
        im3_pos = (40, 1620, 1320, 2340)
        im4_pos = (40, 2400, 1320, 3120)
        positions = [im1_pos, im2_pos, im3_pos, im4_pos]
        return positions
    elif orientation == 'V':
        im1_pos = (60, 40, 780, 1320)
        im2_pos = (840, 40, 1560, 1320)
        im3_pos = (1620, 40, 2340, 1320)
        im4_pos = (2400, 40, 3120, 1320)
        positions = [im1_pos, im2_pos, im3_pos, im4_pos]
        return positions

def single_stripper(strip_code, *args, **kwargs):
    n = 0
    today = datetime.date.today()
    photo_strip = PhotoStrip.objects.get(strip_code=strip_code)
    if photo_strip.strip_half:
        return("Download version already created at " + photo_strip.strip_half.url)
    else:
        pass
    orientation = photo_strip.orientation
    positions = get_coorder(orientation)
    photos = Photo.objects.filter(photo_strip=photo_strip)
    if photo_strip.orientation == 'H':
        im = Image.open("half.jpg")
    elif photo_strip.orientation == 'V':
        im = Image.open("Vhalf.jpg")
    if photos.count() != 4:
        raise ValueError('4 photos are needed to make a strip.') 
    for photo in photos:
        single_im = Image.open(photo.strip_image.path)
        single_im = single_im.convert('RGB')
        im.paste(single_im, positions[n])
        n = n + 1
    im_io = BytesIO()
    font = ImageFont.truetype("BebasNeue-Regular.ttf", 64)
    printed_date = today.strftime("%d %b %Y")
    d = ImageDraw.Draw(im)
    if photo_strip.orientation == 'H':
        d.text((40, 3880), printed_date, fill=(0,0,0), font=font) 
    elif photo_strip.orientation == 'V':
        d.text((3200, 1200), printed_date, fill=(0,0,0), font=font) 
    im.save(im_io, format='JPEG')
    image_file = InMemoryUploadedFile(im_io, None, 'something.jpg', 'image/jpeg', im_io.__sizeof__(), None)
    photo_strip.strip_half.save("dl-{}.jpg".format(strip_code), image_file)
    photo_strip.save()
    half_path = photo_strip.strip_half.path
    return half_path
 
def big_stripper(strip_code, *args, **kwargs):
    photo_strip = PhotoStrip.objects.get(strip_code=strip_code)
    if photo_strip.strip_whole:
        return("Print version already created at " + photo_strip.strip_whole.url)
    else:
        pass
    if photo_strip.strip_half:
        half_path = photo_strip.strip_half.path
    else:
        half_path = single_stripper(strip_code)
    orientation = photo_strip.orientation
    single_strip = Image.open(half_path)
    if photo_strip.orientation == 'H':
        pos1 = (20, 0, 1380, 4080) 
        pos2 = (1380, 0, 2740, 4080) 
        #These are the original coordinates.  Nudge the X or Y values to calibrate your printer.
        #pos1 = (0, 0, 1360, 4080) 
        #pos2 = (1360, 0, 2720, 4080) 
        im = Image.open("whole.jpg")
    elif photo_strip.orientation == 'V':
        pos1 = (0,  0, 4080, 1360) 
        pos2 = (0, 1360, 4080, 2720) 
        im = Image.open("Vwhole.jpg")
    im.paste(single_strip, pos1)
    im.paste(single_strip, pos2)
    im_io = BytesIO()
    im.save(im_io, format='JPEG')
    image_file = InMemoryUploadedFile(im_io, None, 'something.jpg', 'image/jpeg', im_io.__sizeof__(), None)
    photo_strip.strip_whole.save("print-{}.jpg".format(strip_code), image_file)
    photo_strip.save()

def four_square(strip_code, *args, **kwargs):
    n = 0
    photo_strip = PhotoStrip.objects.get(strip_code=strip_code)
    if photo_strip.strip_half:
        return("Print version already created at " + photo_strip.strip_half.url)
    else:
        pass
    positions = get_four_square()
    photos = Photo.objects.filter(photo_strip=photo_strip)
    im = Image.open("four_square_background.jpg")
    im = im.convert('RGB')
    for photo in photos:
        single_im = Image.open(photo.strip_image.path)
        single_im = single_im.convert('RGB')
        print(ImageChops.difference(im, single_im))
        print(im.size, single_im.size)
        im.paste(single_im, positions[n])
        n = n + 1
    im_io = BytesIO()
    im.save(im_io, format='JPEG')
    image_file = InMemoryUploadedFile(im_io, None, 'something.jpg', 'image/jpeg', im_io.__sizeof__(), None)
    photo_strip.strip_half.save("dl-{}.jpg".format(strip_code), image_file)
    photo_strip.save()
    half_path = photo_strip.strip_half.path
    return half_path

def back_print(strip_code, *arg, **kwargs):
    photo_strip = PhotoStrip.objects.get(strip_code=strip_code)
    today = datetime.date.today()
    if photo_strip.strip_whole:
        return("Print version already created at " + photo_strip.strip_whole.url)
    else:
        pass
    im = Image.open("back_print.jpeg")
    im_io = BytesIO()
    font = ImageFont.truetype("BebasNeue-Regular.ttf", 160)
    printed_date = today.strftime("%d %b %Y")
    strip_code = photo_strip.strip_code
    d = ImageDraw.Draw(im)
    d.text((440, 2260), strip_code, fill=(0,0,0), font=font) 
    im.save(im_io, format='JPEG')
    image_file = InMemoryUploadedFile(im_io, None, 'something.jpg', 'image/jpeg', im_io.__sizeof__(), None)
    photo_strip.strip_whole.save("dl-{}.jpg".format(strip_code), image_file)
    photo_strip.save()
    whole_path = photo_strip.strip_whole.path
    return whole_path 
