from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
import json, logging
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, Room

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        logger.info(f"WebSocket connection attempt: room={self.room_id}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket connected: room={self.room_id}")

        # Send existing messages to the client
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message
            }))

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: room={self.room_id}, code={close_code}")

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def get_messages(self):
        room = Room.objects.get(name=self.room_id)
        return list(Message.objects.filter(room=room).order_by('-timestamp').values('id', 'user__username', 'text', 'timestamp'))

    @sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=self.room_id)
        return Message.objects.create(user=user, room=room, text=message)

    async def receive(self, text_data):
        logger.info(f"WebSocket message received: room={self.room_id}, data={text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        message_obj = await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message_obj.id,
                    'user__username': username,
                    'text': message,
                    'timestamp': str(message_obj.timestamp)
                }
            }
        )


    async def chat_message(self, event):
        message = event['message']
        logger.info(f"Sending message to WebSocket: room={self.room_id}, message={message}")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))