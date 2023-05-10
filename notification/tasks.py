from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from .models import NotificationModel
from celery import Celery
from celery.exceptions import Ignore
from add.tests import pint
import asyncio
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

@shared_task(bind=True)
def broadcast_notifiation_task(self, pk, table_key, channel_name):    
    print(channel_name, "notidication task")
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for c in channel_name:
        loop.run_until_complete(
            channel_layer.send(
            c,
            {
            "type":"notification.send",
            "notification_msg":json.dumps({"offerd_price_pk":table_key, "notification_table_key":pk})
            }
            )
        )