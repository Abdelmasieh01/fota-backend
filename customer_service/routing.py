from django.urls import re_path

from . import consumers

app_name = 'customer_service'

websocket_urlpatterns = [
    re_path(r'ws/queue/', consumers.QueueConsumer.as_asgi(), name='queue'),
    re_path(r'ws/chat/', consumers.ChatConsumer.as_asgi(), name='chat'),
]
