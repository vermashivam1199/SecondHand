from add.models import OfferedPrice
from .models import NotificationModel
from django.db.models.signals import post_save
from django.dispatch import receiver 
from add.tests import pint
from .tasks import broadcast_notifiation_task
from channels.layers import get_channel_layer
from user_profile.tasks import broadcast_dashboard_task
import json

@receiver(post_save, sender=OfferedPrice)
def offered_price_handler(sender, instance, created, **kwargs):
    if created:
        pint("offered price signal")
        row = NotificationModel(
            notification_msg = f"{instance.id}",
            concerned_tabel_key = f"{instance.id}",
            receiver = instance.add.owner, 
            sender = instance.owner,
            table_name = "OfferedPrice"
        )
        pint(row, "notification object")
        pint("offered price signal sender====", instance.owner)
        pint("offered price signal reciver====", instance.add.owner.username)
        row.save()

        #dashboard handler
        channel_name = list(instance.add.owner.channel_name.filter(consumer_name="DashboardConsumer"))
        channel_name = [c.channel_name for c in channel_name]

        comment_date = str(instance.created_at.date())
        add_id = instance.add.id
        table_name = "OfferedPrice"
        pint(channel_name, "OfferedPrice signal")
        pint(comment_date)
        broadcast_dashboard_task.delay(channel_name=channel_name, date_data=comment_date, table_name=table_name, add_id=add_id)
    else:
        pint("offered price signal")
        row = NotificationModel(
            notification_msg = f"{instance.id}",
            concerned_tabel_key = f"{instance.id}",
            receiver = instance.add.owner, 
            sender = instance.owner,
            table_name = "OfferedPrice"
        )
        pint(row, "notification object")
        pint("offered price signal sender====", instance.owner)
        pint("offered price signal reciver====", instance.add.owner.username)
        row.save()



@receiver(post_save, sender=NotificationModel)
def notification_handler(sender, instance, created, **kwargs):
    pint("notification model working")
    pint("offered price signal",instance.id)
    pint("offered price signal",instance.notification_msg)
    pint("notification signal ",instance.receiver.channel_name.all().first().channel_name)
    channel_name = list(instance.receiver.channel_name.filter(consumer_name="OfferedPriceConsumer"))
    channel_name = [c.channel_name for c in channel_name]
    broadcast_notifiation_task.delay(pk=str(instance.id), channel_name=channel_name, table_key=instance.concerned_tabel_key)
