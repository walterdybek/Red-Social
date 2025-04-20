# base/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Room, Message, User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        
        # Guardar el mensaje en la base de datos
        user = await sync_to_async(User.objects.get)(id=user_id)
        room = await sync_to_async(Room.objects.get)(id=self.room_id)
        
        message_obj = await sync_to_async(Message.objects.create)(
            user=user,
            room=room,
            body=message
        )
        
        # Enviar mensaje a room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': str(message_obj.id),
                'message': message,
                'user_id': user.id,
                'username': user.username,
                'avatar': user.avatar.url if user.avatar else '',
                'created': timezone.now().isoformat(),
            }
        )

    async def chat_message(self, event):
        # Enviar mensaje a WebSocket
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'message': event['message'],
            'user_id': event['user_id'],
            'username': event['username'],
            'avatar': event['avatar'],
            'created': event['created'],
        }))