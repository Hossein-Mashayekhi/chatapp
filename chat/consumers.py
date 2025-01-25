import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"[DEBUG] WebSocket connected to room: {self.room_name}")

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"[DEBUG] WebSocket disconnected from room: {self.room_name}")
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Parse the received message
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender']
        print(f"[DEBUG] Received message: {message} from {sender_username}")

        # Get sender and recipient
        sender = await database_sync_to_async(User.objects.get)(username=sender_username)
        recipient = await database_sync_to_async(User.objects.get)(username=self.room_name)

        # Save the message to the database
        await database_sync_to_async(Message.objects.create)(
            sender=sender,
            recipient=recipient,
            content=message
        )

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket clients
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
