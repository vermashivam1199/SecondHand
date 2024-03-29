from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from add.tests import pint
from .models import ChannelName, NotificationModel
import asyncio
from asgiref.sync import sync_to_async
import json
from add.models import OfferedPrice, Add
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer



class OfferedPriceConsumer(AsyncConsumer):

    @sync_to_async
    def offer_price_list(self,user):
        o = OfferedPrice.objects.filter(owner=user)
        return [i.add.owner.username for i in o]
    
    @sync_to_async
    def channel_name_funk(self):
        row = ChannelName(owner=self.user, consumer_name="OfferedPriceConsumer", channel_name=self.channel_name)
        row.save()
        self.channel_id = row.id # saving instance id of current notification channel_name table

    @sync_to_async
    def channel_name_delete(self):
        rows = ChannelName.objects.get(pk=self.channel_id)
        pint(rows, "notification delete")
        rows.delete()  

    @sync_to_async
    def final_msg_funk(self):
        return {
            "sender": str(self.notification_row.sender.username),
            "time": str(self.notification_row.broadcast_time),
            "add": str(self.offered_price.add.id)
        }


    async def websocket_connect(self, event):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
        # saving channel name  
            await self.channel_name_funk()    
            self.owner_group_name = self.user.username
            await self.channel_layer.group_add(self.owner_group_name, self.channel_name)
            for i in await self.offer_price_list(self.user):
                await self.channel_layer.group_add(str(i), self.channel_name)
                pint('offered price consumer groupname======',i)
                pint("offered price consumer current user=====", self.user)
            await self.send({
                "type":"websocket.accept"
            })  

    async def websocket_recive(self, event):
        ...

    async def websocket_disconnect(self, event):
        if self.user.is_authenticated:
            await self.channel_name_delete()
        raise StopConsumer
    
    async def notification_send(self, event):
        msg = json.loads(event["notification_msg"])
        pint("notification_send consumer", msg)
        self.offered_price = await sync_to_async(get_object_or_404)(OfferedPrice, pk=int(msg["offerd_price_pk"]))
        self.notification_row = await sync_to_async(get_object_or_404)(NotificationModel, pk=int(msg["notification_table_key"]))
        final_msg = await self.final_msg_funk()
        pint(final_msg)
        await self.send({
                "type":"websocket.send",
                "text":json.dumps(final_msg)
            })
        



