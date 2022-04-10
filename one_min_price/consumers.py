import json

from channels.generic.websocket import AsyncWebsocketConsumer

from one_min_price.tasks import up_down


class WSConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        await self.send(json.dumps({'message': up_down.delay(text_data['symbol'], float(text_data['price'])).get()}))
        # return await super().receive(text_data, bytes_data)
