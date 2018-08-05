import json
from channels.generic.websocket import AsyncWebsocketConsumer
from utils import redis, redis_uid_results_expiry_time_in_seconds as r_uid_ex
from utils.helpers import serialize, deserialize


class LogServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'log_servers'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        self.ip = None
        await self.accept()
        # print("connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        if self.ip is not None:
            log_servers = deserialize(redis.get('log_servers'))
            log_servers.discard(self.ip)
            redis.set('log_servers', serialize(log_servers))
        # print("disconnected")

    async def receive(self, text_data):
        # print(text_data)
        data = json.loads(text_data)
        if data['type'] == 'server_info':
            ip = data['ip']
            self.ip = ip
            log_servers = deserialize(redis.get('log_servers'))
            if not log_servers.isdisjoint([ip]):
                return await self.disconnect(1000)
            log_servers.add(ip)
            redis.set('log_servers', serialize(log_servers))
        elif data['type'] == 'log_result':
            # print('at log server consumer log_result')
            cached_results = deserialize(redis.get(f"results-{data['uid']}"))
            cached_results[data['ip']] = data['result']
            redis.set(f"results-{data['uid']}",
                      serialize(cached_results), ex=r_uid_ex)
            await self.channel_layer.group_send('log_clients', data)

    async def log_query(self, event):
        # TODO covert everything to json
        # here send_json
        redis.set(f"results-{event['uid']}", serialize({}))
        await self.send(json.dumps(event))


# FIXME channel's urlpatterns @ routing.py


class LogClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.uid = self.scope['url_route']['kwargs']['uid']
        self.group_name = 'log_clients'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("got at `receive`")
        # data = json.loads(text_data)
    #     if data['type'] == 'log_result':
    #         await self.send(json.dumps({
    #             'ip': data['ip'],
    #             'result': data['result']
    #         }))
    #         #     # TODO check if self.uid matched with data, if yes then send
        #     # hey hey, but aayega kaise? log_server to sirf LogServerConsumer se baat karta hai

        #     if data['uid'] == self.uid:
        #         await self.send(text_data)

    async def log_result(self, event):
        if self.uid == event['uid']:
            await self.send(json.dumps({
                'ip': event['ip'],
                'result': event['result']
            }))
