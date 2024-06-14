import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Queue


class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = 'queue'
        user = self.scope["user"]
        self.user_positions = {}
        if user.is_authenticated:
            user_queue = await sync_to_async(lambda: getattr(user, 'queue', None), thread_sensitive=True)()
            if user_queue:
                print(user_queue)
                await delete_queue_object(user)

            queue = Queue(user=user)
            report_id = (dict((x.split('=') for x in self.scope['query_string'].decode().split(
                "&")))).get('report_id', None)
            if report_id:
                queue.report = report_id
            await queue.asave()

            await self.channel_layer.group_add(
                self.room, self.channel_name
            )
            await self.accept()

            # Notify the user of their position in the queue
            await self.notify_user_position(user)
            # Notify all users in the queue about their updated positions
            await self.channel_layer.group_send(
                self.room, {"type": "queue.update_positions"}
            )

        else:
            await self.close()

    async def disconnect(self, code):
        user = self.scope["user"]
        if user.is_authenticated:
            await delete_queue_object(user)

            await self.channel_layer.group_discard(
                self.room, self.channel_name
            )

            # Notify all users in the queue about their updated positions
            await self.channel_layer.group_send(
                self.room, {"type": "queue.update_positions"}
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room, {"type": "queue.message", "message": message}
        )

    # Receive message from room group
    async def queue_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def notify_user_position(self, user):
        user_queue = await sync_to_async(lambda: getattr(user, 'queue', None), thread_sensitive=True)()
        if user_queue:
            position = await self.get_user_position(user_queue)
            last_position = self.user_positions.get(user.id)
            if last_position != position:
                self.user_positions[user.id] = position
                await self.send(text_data=json.dumps({
                    "message": f"You are number {position} in the queue."
                }))

    async def queue_update_positions(self, event):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.notify_user_position(user)

    @database_sync_to_async
    def get_user_position(self, user_queue):
        return Queue.objects.filter(timestamp__lt=user_queue.timestamp).count() + 1


@database_sync_to_async
def delete_queue_object(user):
    Queue.objects.filter(user=user).delete()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = 'chat'
        user = self.scope['user']
        if user.is_authenticated:
            await self.channel_layer.group_add(
                self.room, self.channel_name
            )
            await self.channel_layer.group_send(
                self.room, {
                    'type': 'chat.start',
                    'is_customer_service': user.is_customer_service
                }
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)

    async def chat_start(self, event):
        user = self.scope['user']
        joined_user_is_customer_service = event['is_customer_service']
        if user.is_customer_service and not joined_user_is_customer_service:
            await self.send(text_data=json.dumps({'message': 'A customer has joined the chat.'}))
        elif not user.is_customer_service and joined_user_is_customer_service:
            await self.send(text_data=json.dumps({
                'message': 'A customer service representative joined the chat. You can start talking now!'
            }))

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message']
        user_id = self.scope['user'].id
        await self.channel_layer.group_send(self.room, {
            'type': 'chat.message',
            'message': message,
            'user_id': user_id
        })

    async def chat_message(self, event):
        message = event['message']
        message_user_id = event['user_id']
        user_id = self.scope['user'].id

        if message_user_id != user_id:
            await self.send(text_data=json.dumps({'message': message}))
