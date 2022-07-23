from django.core.management import BaseCommand
from django.conf import settings
from app.models import Account
from time import *
from random import randint as random
import os, uvloop, asyncio, aiohttp

post_text = "ATTENTION❗ Каждый кто сделает репост данной записи, получит на свой игровой акканут "
TOKEN = "ABOBA"
GROUP_ID = "-ABOBA"
V = '5.120'
API = 'https://api.vk.com/method'
METHOD = 'wall.post'
METHOD_TWO = 'wall.getReposts'
METHOD_THREE = 'messages.send'
METHOD_FOUR = "wall.createComment"
METHOD_FIVE = "wall.closeComments"
TOKEN_MESSAGE = 'ABOBA'
PHOTO = ['photo-198059264_457239518', 'photo-198059264_457239519', 'photo-198059264_457239520', "photo-198059264_457239521", 'photo-198059264_457239522']

class Command(BaseCommand):

    def handle(self, *args, **options):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.ioloop = asyncio.get_event_loop() 
        self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.autopost())]))
        self.ioloop.close()
    
    async def autopost(self):
        response_json = None
        session = aiohttp.ClientSession()
        points = 0
        while True:
            points = random(2, 5)
            params = {'access_token': TOKEN,'group_id': GROUP_ID,'v': V,'owner_id': GROUP_ID, 'from_group': 1, 'message': post_text + f"{points}" + (" баллов" if points == 5 else " балла") + ", акция действует ровно сутки.", 'attachment': PHOTO[points-1]}
            async with session.post(f"{API}/{METHOD}", params = params) as response:
                response_json = await response.json()

            params = {'access_token': TOKEN,
    			  'group_id': GROUP_ID,
    			  'v': V,
    			  'owner_id': GROUP_ID, 
    			  'post_id': response_json['response']['post_id'], 
    			  'from_group': GROUP_ID.replace("-", ""),
    			  'message': "‼ Баллы будут выданы по окончанию акции, ваш профиль VK должен быть открыт, а то мы не увидим Ваш репост."}

            async with session.post(f"{API}/{METHOD_FOUR}", params = params) as response:
                print(await response.json())

            params = {'access_token': TOKEN,
    			  'group_id': GROUP_ID,
    			  'v': V,
    			  'owner_id': GROUP_ID, 
    			  'post_id': response_json['response']['post_id']}

            async with session.post(f"{API}/{METHOD_FIVE}", params = params) as response:
                print(await response.json())

            sleep(86400)
            params = {'access_token': TOKEN,'group_id': GROUP_ID,'v': V, 'owner_id': GROUP_ID, 'post_id': response_json['response']['post_id']}
            async with session.post(f"{API}/{METHOD_TWO}", params = params) as response:
                users = await response.json()
                users = users['response']['profiles']
                if len(users) != 0:
                    for user in users:
                        try:
                            game_account = Account.objects.get(user_id=user['id'])
                            game_account.donate_points += points
                            game_account.save()
                            params = {'user_id': game_account.user_id,
                            'message': f"Спасибо за участие в акции! Вы получили {points} {' баллов' if points == 5 else ' балла'} за репост",
                            'random_id': random(10000, 100000000)}
                            params.update({'access_token': TOKEN_MESSAGE, 'group_id': GROUP_ID.replace('-',''), 'v': V})
                            async with session.post(f"{API}/{METHOD_THREE}", params = params) as response:
                               print(await response.json())
                        except:
                            continue
                break
        