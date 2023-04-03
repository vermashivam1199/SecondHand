from add.models import OfferedPrice
from .models import NotificationModel
from django.db.models.signals import post_save
from django.dispatch import receiver 
from add.tests import pint
from .tasks import broadcast_notifiation_task
from channels.layers import get_channel_layer

@receiver(post_save, sender=OfferedPrice)
def offered_price_handler(sender, instance, created, **kwargs):
    pint("offered price signal")
    if created:
        row = NotificationModel(
            notification_msg = "...",
            concerned_tabel_key = f"{instance.id}",
            receiver = instance.add.owner, 
            sender = instance.owner
        )
    else:
        row = NotificationModel(
            notification_msg = "...",
            concerned_tabel_key = f"{instance.id}",
            receiver = instance.add.owner,
            sender = instance.owner
        )
    row.save()
    # pint("offered price signal sender====", instance.owner)
    # pint("offered price signal reciver====", instance.add.owner.username)


@receiver(post_save, sender=NotificationModel)
def notification_handler(sender, instance, created, **kwargs):
    # pint("notification model working")
    # pint("offered price signal",instance.id)
    # pint("offered price signal",instance.notification_msg)
    pint("notification signal ",instance.receiver.channel_name.all().first().channel_name)
    broadcast_notifiation_task.delay(pk=instance.id)