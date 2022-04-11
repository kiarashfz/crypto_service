import json

from channels.generic.websocket import AsyncWebsocketConsumer

from one_min_price.tasks import up_down


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_group_name = self.scope['url_route']['kwargs']['channel_name']

        await self.channel_layer.group_add(
            self.channel_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.channel_group_name,
            {
                'type': 'channel_message',
                'message': up_down.delay(text_data['symbol'], float(text_data['price'])).get()
            }
        )

    async def channel_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
