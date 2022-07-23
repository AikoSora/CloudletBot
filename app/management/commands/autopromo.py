from django.core.management import BaseCommand
from django.conf import settings
from app.models import Account, Promo
from time import *
from random import randint as random
import os, uvloop, asyncio, aiohttp

max_users = 5
price = 100
promo_name = "бабло"
#https://oauth.vk.com/authorize?client_id=7625769&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,offline&response_type=token&v=5.120&state=123456
post_text_one = f"ATTENTION❗ Первые {max_users} игроков, написавших боту в ЛС <<промо {promo_name}>>, получат {price}$ на свой аккаунт!"
TOKEN = "ABOBA"
GROUP_ID = "-ABOBA"
V = '5.120'
API = 'https://api.vk.com/method'
METHOD = 'wall.post'
PHOTO = "doc338845100_586143767"

class Command(BaseCommand):

    def handle(self, *args, **options):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.ioloop = asyncio.get_event_loop() 
        self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.autopromo())]))
        self.ioloop.close()
    
    async def autopromo(self):
        sleep(random(0, 600))
        params = {'access_token': TOKEN,'group_id': GROUP_ID,'v': V,'owner_id': GROUP_ID, 'from_group': 1, 'message': post_text_one, 'attachment': PHOTO}

        session = aiohttp.ClientSession()
        async with session.post(f"{API}/{METHOD}", params = params) as response:
            print(await response.json())
        promo = Promo.objects.filter(name=promo_name).first()
        print(promo)
        if promo is not None:
            promo.activated = 0
            promo.id += 1
            Promo.objects.filter(id=(promo.id-1)).delete()
            promo.save()
        else:
            Promo.objects.create(name=promo_name, max_users=max_users, price=price)
        await session.close()
        
