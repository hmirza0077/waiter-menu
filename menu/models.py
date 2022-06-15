from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


channel = get_channel_layer()


class Desk(models.Model):
    code = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.category.title}"


class Requests(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)


@receiver(post_save, sender=Requests)
def send_notif(sender, instance, **kwargs):
    async_to_sync(channel.group_send)(instance.desk.code, {'type': 'request_waiter', 'code': instance.desk.code})
