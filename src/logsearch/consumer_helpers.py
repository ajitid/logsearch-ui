from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


def send_to_group_sync(group_name, data):
    async_to_sync(channel_layer.group_send)(group_name, data)
