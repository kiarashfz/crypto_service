import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django_celery_beat.models import IntervalSchedule, PeriodicTask


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
        schedule, created = await sync_to_async(IntervalSchedule.objects.get_or_create)(
            every=1,
            period=IntervalSchedule.MINUTES,
        )

        self.task, created = await sync_to_async(PeriodicTask.objects.get_or_create)(
            interval=schedule,
            name=f'{self.channel_group_name}',
            task='one_min_price.tasks.up_down',
            kwargs=json.dumps({
                'symbol': text_data['symbol'],
                'price': float(text_data['price']),
                'channel_group_name': self.channel_group_name,
            }),
        )

    async def channel_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, code):
        self.task.enabled = False
        await sync_to_async(self.task.save)()
        return await super().disconnect(code)
