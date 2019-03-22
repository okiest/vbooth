import asyncio
import json
import base64
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from django.core.files.base import ContentFile

from strip.models import *

demo_strip = PhotoStrip.objects.get(pk=1)

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
        await self.save_photo(event)
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_data = json.loads(event_text)
            loaded_img = loaded_data.get('imgBase64')
        

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
