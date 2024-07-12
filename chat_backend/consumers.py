from channels.generic.websocket import AsyncWebsocketConsumer
import json, logging
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, Room
from channels.layers import get_channel_layer
import asyncio

logger = logging.getLogger(__name__)
channel_layer = get_channel_layer()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']

        logger.info(f"WebSocket connection attempt: room={self.room_id}, user={self.user}")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"WebSocket connected: room={self.room_id}, user={self.user}")

        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'type': 'chat_history',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: room={self.room_id}, user={self.user}, code={close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'chat_message':
            message = data['message']
            username = data['username']
            message_obj = await self.save_message(username, message)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message_obj.id,
                        'user__username': username,
                        'text': message,
                        'created_at': str(message_obj.created_at.isoformat())
                    }
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))

    @sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(id=self.room_id)
        return Message.objects.create(user=user, room=room, text=message)

    @sync_to_async
    def get_messages(self):
        room = Room.objects.get(id=self.room_id)
        messages = Message.objects.filter(room=room).order_by('created_at').values('id', 'user__username', 'text', 'created_at')
        return [{**msg, 'created_at': msg['created_at'].isoformat()} for msg in messages]

class RoomListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("room_list", self.channel_name)
        await self.accept()
        await self.send_room_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("room_list", self.channel_name)

    async def room_list_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'room_list_update',
            'rooms': event['rooms']
        }))

    async def send_room_list(self):
        rooms = await self.get_all_rooms()
        await self.send(text_data=json.dumps({
            'type': 'room_list_update',
            'rooms': rooms
        }))

    @sync_to_async
    def get_all_rooms(self):
        return list(Room.objects.all().values('id', 'name'))

async def notify_room_list_update():
    rooms = await RoomListConsumer().get_all_rooms()
    await channel_layer.group_send(
        "room_list",
        {
            "type": "room_list_update",
            "rooms": rooms
        }
    )

@sync_to_async
def create_room(name):
    room = Room.objects.create(name=name)
    asyncio.create_task(notify_room_list_update())
    return room