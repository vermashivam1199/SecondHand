from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from celery import Celery
from celery.exceptions import Ignore
from add.tests import pint
import asyncio
import json
from add.models import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

@shared_task(bind=True)
def broadcast_dashboard_task(self, channel_name, **kwargs):
    pint(channel_name, "dashboard task")
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    pint(kwargs)
    for c in channel_name:
        pint(c)
        loop.run_until_complete(
            channel_layer.send(
            c,
            {
            "type":"dashbord.send",
            "notification_msg":json.dumps(kwargs)
            }
            )
        )
    