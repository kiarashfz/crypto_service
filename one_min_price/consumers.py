import json
from random import randint
from time import sleep

from channels.generic.websocket import WebsocketConsumer

from one_min_price.tasks import add


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(1000):
            func = add.delay(randint(1, 10), randint(1, 10))
            res = func.get()
            self.send(json.dumps({'message': res}))
            sleep(1)
