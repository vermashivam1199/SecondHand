from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from add.tests import pint
import asyncio
from asgiref.sync import sync_to_async
from .models import Group, ChatModel
import json

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        pint('websocket connected', event)
        await self.send({
            "type":"websocket.accept"
        })
        self.group_name = self.scope['url_route']['kwargs']['g_name']
        pint(self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        pint('connection accepted', event)

    async def websocket_receive(self, event):
        
        pint(event)
        await self.save_chat(event['text'])
        await self.channel_layer.group_send(self.group_name, {
            'type':'chat.msg',
            'msg':event["text"],
        })
        pint('message recived', event)
    
    async def chat_msg(self, event):
        pint('chat_msg=========',event)
        await self.send({
            "type":"websocket.send",
            "text": event['msg']
        })

    async def websocket_disconnect(self, event):
        # pint('websocket disconnected', event)
        raise StopConsumer

    @sync_to_async
    def save_chat(self, msg):
        pint('working')
        message = json.loads(msg)
        pint(message)
        group = Group.objects.get(group_name=self.group_name)
        chat = ChatModel(message=message['msg'], user=self.scope['user'], group=group)
        chat.save()