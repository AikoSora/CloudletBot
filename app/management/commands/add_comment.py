from django.core.management import BaseCommand
from django.conf import settings
from app.models import Account
from time import *
from random import randint as random
import os, uvloop, asyncio, aiohttp

TOKEN = "ABOBA"
GROUP_ID = "-ABOBA"
V = '5.120'
API = 'https://api.vk.com/method'
METHOD = "wall.createComment"
METHOD_TWO = "wall.closeComments"

class Command(BaseCommand):

    def handle(self, *args, **options):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.ioloop = asyncio.get_event_loop() 
        self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.autopost())]))
        self.ioloop.close()
    
    async def autopost(self):
        session = aiohttp.ClientSession()

        params = {'access_token': TOKEN,
    			  'group_id': GROUP_ID,
    			  'v': V,
    			  'owner_id': GROUP_ID, 
    			  'post_id': 55, 
    			  'from_group': GROUP_ID.replace("-", ""),
    			  'message': "‼ Баллы будут выданы по окончанию акции, ваш профиль VK должен быть открыт, а то мы не увидим Ваш репост."}

        async with session.post(f"{API}/{METHOD}", params = params) as response:
                print(await response.json())

        params = {'access_token': TOKEN,
    			  'group_id': GROUP_ID,
    			  'v': V,
    			  'owner_id': GROUP_ID, 
    			  'post_id': 55}

        async with session.post(f"{API}/{METHOD_TWO}", params = params) as response:
                print(await response.json())