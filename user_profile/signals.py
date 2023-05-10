from add.models import AddHistory, Comment, OfferedPrice, Saved
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from add.tests import pint
from channels.layers import get_channel_layer
from .tasks import broadcast_dashboard_task
import json


@receiver(post_save, sender=Comment)
def comments_handler(sender, instance, created, **kwargs):
    channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    comment_date = str(instance.created_at.date())
    add_id = instance.add.id
    
    table_name = "Comment"
    pint(channel_name, "comment signal")
    pint(comment_date)
    broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id)

@receiver(post_save, sender=AddHistory)
def add_history_handler(sender, instance, created, **kwargs):
    channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    pint("xxxxxxxxxxxx add history", channel_name, "xxxxxxxxxxx")
    comment_date = str(instance.created_at.date())
    add_id = instance.add.id
    table_name = "AddHistory"
    pint(channel_name, "AddHistory signal")
    pint(comment_date)
    broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id)

@receiver(post_save, sender=Saved)
def saved_handler(sender, instance, created, **kwargs):
    channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    comment_date = str(instance.created_at.date())
    add_id = instance.add.id
    
    table_name = "Saved"
    pint(channel_name, "Saved signal")
    pint(comment_date)
    broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id)

@receiver(post_delete, sender=OfferedPrice)
def offer_price_delete_handler(sender, instance, **kwargs):
    channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    comment_date = str(instance.created_at.date())
    add_id = instance.add.id
    
    table_name = "OfferedPrice"
    pint(channel_name, "OfferedPrice signal")
    pint(comment_date)
    broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id, dele=True)

@receiver(post_delete, sender=Saved)
def saved_handler(sender, instance, **kwargs):
    channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    comment_date = str(instance.created_at.date())
    add_id = instance.add.id
    
    table_name = "Saved"
    pint(channel_name, "Saved signal")
    pint(comment_date)
    broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id,  dele=True)


@receiver(post_delete, sender=Comment)
def comment_handler(sender, instance, **kwargs):
    channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    comment_date = str(instance.created_at.date())
    add_id = instance.add.id
    
    table_name = "Comment"
    pint(channel_name, "comment signal")
    pint(comment_date)
    broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id, dele=True)