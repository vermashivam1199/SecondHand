from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from add.tests import pint
import asyncio
from asgiref.sync import sync_to_async
import json
from add.models import OfferedPrice, Add
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer
from notification.models import ChannelName




class DashboardConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            pint("dashboard consumer")
            await self.channel_name_funk()
            await self.send({
            "type":"websocket.accept"
        })

    async def websocket_recive(self, event):
        ...

    async def websocket_disconnect(self, event):
        if self.user.is_authenticated:
            await self.channel_name_delete()
        raise StopConsumer
            
    async def dashbord_send(self, event):
        pint(event, "broadcast event")
        await self.send({
                "type":"websocket.send",
                "text":event["notification_msg"]
            })

    
    @sync_to_async
    def channel_name_funk(self):
        row = ChannelName(owner=self.user, consumer_name="DashboardConsumer", channel_name=self.channel_name)
        row.save()
        self.channel_id = row.id
    
    @sync_to_async
    def channel_name_delete(self):
        rows = ChannelName.objects.get(pk=self.channel_id)
        pint(rows, "dashboard delete")
        rows.delete()