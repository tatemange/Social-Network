import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from accounts.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Ensure user is authenticated
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        # Check if user is participant of the discussion
        is_participant = await self.is_user_participant(self.room_name, self.scope['user'])
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Set user online status
        await self.set_online_status(self.scope['user'], True)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Set user offline status
        if 'user' in self.scope and self.scope['user'].is_authenticated:
            await self.set_online_status(self.scope['user'], False)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get('message', '')

        if not message_content.strip():
            return

        user = self.scope['user']
        
        # Save message to database
        saved_msg = await self.save_message(self.room_name, user, message_content)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'expediteur_id': user.id,
                'expediteur_nom': user.prenom,
                'date': saved_msg.dateEnvoi.strftime('%H:%M')
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        expediteur_id = event['expediteur_id']
        expediteur_nom = event['expediteur_nom']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'expediteur_id': expediteur_id,
            'expediteur_nom': expediteur_nom,
            'date': date
        }))

    @database_sync_to_async
    def is_user_participant(self, discussion_id, user):
        try:
            discussion = Conversation.objects.get(id=discussion_id)
            return discussion.participants.filter(user=user).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, discussion_id, user, content):
        discussion = Conversation.objects.get(id=discussion_id)
        return Message.objects.create(
            discussion=discussion,
            expediteur=user,
            contenu=content,
            typeMessage='texte'
        )

    @database_sync_to_async
    def set_online_status(self, user, is_online):
        try:
            # Refresh user from DB to avoid caching issues
            db_user = CustomUser.objects.get(id=user.id)
            db_user.statutEnLigne = is_online
            db_user.save(update_fields=['statutEnLigne'])
        except CustomUser.DoesNotExist:
            pass
