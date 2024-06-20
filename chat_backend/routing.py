from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat_backend import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/messages/', consumers.MessageConsumer.as_asgi()),
    ]),
})