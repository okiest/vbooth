import asyncio
import json
import base64
from PIL import Image
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile

from utils.stripper import *

from strip.models import *

global new_strip

class FahkeekConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        global new_strip
        new_strip = PhotoStrip(strip_date=timezone.now())
        new_strip.save()


    async def websocket_receive(self, event):
        finished = False
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            try:
                create_new = loaded_data.get('new_strip')
                await self.new_strip(event)
            except:
                finished = False
            try:
                loaded_img = loaded_data.get('imgBase64')
                await self.save_photo(event)
            except:
                finished = False
            try:
                finished = loaded_data.get('strip_done')
            except:
                finished = False
            print("Finished: ", finished)
            if finished is True:
                new_url = "/lobby/" + new_strip.strip_code
                photos = Photo.objects.filter(photo_strip=new_strip)
                im = Image.open(photos[0].strip_image.path) 
                width, height = im.size
                if width > height:
                    new_strip.orientation = 'H'
                    new_strip.save()
                else:
                    pass
                single_stripper(new_strip.strip_code)
                myRedirect = {
                    'newURL': new_url,
                }
                print("sending redirect")
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(myRedirect), 
                })
        

    async def websocket_disconnect(self, event):
        print("disconnected", event)


    #@database_sync_to_async
    async def save_photo(self, event, *args, **kwargs):
        print("saving photo...")
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            data = loaded_data.get('imgBase64')
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        new_photo =  Photo(
            photo_strip = new_strip,
            strip_image = data
        )
        new_photo.save()
        return new_photo
    
    async def new_strip(self, event, *args, **kwargs):
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            data = loaded_data.get('new_strip')
            if new_strip is True:
                print("Creating new strip.") 
                new_strip = PhotoStrip(strip_date=timezone.now())
                new_strip.save()
                

class BoothConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        global new_strip
        new_strip = PhotoStrip(strip_date=timezone.now())
        new_strip.save()


    async def websocket_receive(self, event):
        finished = False
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            try:
                create_new = loaded_data.get('new_strip')
                await self.new_strip(event)
            except:
                finished = False
            try:
                loaded_img = loaded_data.get('imgBase64')
                await self.save_photo(event)
            except:
                finished = False
            try:
                finished = loaded_data.get('strip_done')
            except:
                finished = False
            print("Finished: ", finished)
            if finished is True:
                new_url = "/kiosk/lobby/" + new_strip.strip_code
                photos = Photo.objects.filter(photo_strip=new_strip)
                im = Image.open(photos[0].strip_image.path)
                width, height = im.size
                if width > height:
                    new_strip.orientation = 'H'
                    new_strip.save()
                else:
                    pass
                #single_stripper(new_strip.strip_code)
                ## TODO Add poscard post processing
                half_path = four_square(new_strip.strip_code)
                whole_path = back_print(new_strip.strip_code)
                make_printable(half_path, whole_path, strip_code=new_strip.strip_code)
                myRedirect = {
                    'newURL': new_url,
                }
                print("sending redirect")
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(myRedirect),
                })


    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def save_photo(self, event, *args, **kwargs):
        print("saving photo...")
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            data = loaded_data.get('imgBase64')
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        new_photo =  Photo(
            photo_strip = new_strip,
            strip_image = data
        )
        new_photo.save()
        return new_photo

    async def new_strip(self, event, *args, **kwargs):
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            data = loaded_data.get('new_strip')
            if new_strip is True:
                print("Creating new strip.")
                new_strip = PhotoStrip(strip_date=timezone.now())
                new_strip.save()

