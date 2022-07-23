from django.core.management import BaseCommand
from django.conf import settings
from datetime import datetime
from app.models import Account, Hacker, Police, Other
import os, uvloop, asyncio, aiohttp, time, json, sys

TOKEN = 'ABOBA'
STATUS_TOKEN = 'ABOBA'
V = '5.103'
API = "https://api.vk.com/method"
ID = 'ABOBA'
METHOD = 'appWidgets.update'
METHOD_TWO = 'status.set'
sys.stdout = open('/home/Cloudlet/widget.log', 'a')

def digit_number(number):
    return '{0:,}'.format(number).replace(',', '.')

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.ioloop = asyncio.get_event_loop()
        self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.job())]))
        self.ioloop.close()

    async def job(self):
        try:
            json_file = open("/home/Cloudlet/widget_data.json", "r")
            new_widget = json.load(json_file)["new_widget"]
            json_file.close()
        except:
            new_widget = False
        session = aiohttp.ClientSession()
        json_file = open("/home/Cloudlet/widget_data.json", "w+")
        try:
            if new_widget == False:
                CODE = {"title": "Топ хакеров 👾","head": [{"text": "Ник игрока"},{"text": "Рейтинг","align": "right"}],"body": []}
                for user in Hacker.objects.all().order_by("-hacks_count")[:10]:
                    if user.user.hyperlink != 1:
                        CODE['body'].append([{'icon_id': f'id{user.user.user_id}',
                                                      'text': user.user.username,
                                                      'url': f'https://vk.com/id{user.user.user_id}'},
                                                      {'text': f'{digit_number(user.hacks_count)} 👑'}])
                    else:
                        CODE['body'].append([{'icon_id': f'id{user.user.user_id}',
                                              'text': user.user.username},
                                              {'text': f'{digit_number(user.hacks_count)} 👑'}])
                json.dump({"new_widget": True}, json_file)
            else:
                CODE = {"title": "Топ полицейских 🔐","head": [{"text": "Ник игрока"},{"text": "Рейтинг","align": "right"}],"body": []}
                for user in Police.objects.all().order_by("-arrest_count")[:10]:
                    if user.user.hyperlink != 1:
                        CODE['body'].append([{'icon_id': f'id{user.user.user_id}',
                                                      'text': user.user.username,
                                                      'url': f'https://vk.com/id{user.user.user_id}'},
                                                      {'text': f'{digit_number(user.arrest_count)} 👑'}])
                    else:
                        CODE['body'].append([{'icon_id': f'id{user.user.user_id}',
                                              'text': user.user.username},
                                              {'text': f'{digit_number(user.arrest_count)} 👑'}])
                json.dump({"new_widget": False}, json_file)
            NEW_CODE = 'return{};'.format(CODE)
            params = {'access_token': TOKEN,'group_id': ID,'v': V,'type': 'table','code': NEW_CODE}
            async with session.post(f"{API}/{METHOD}", params = params) as response:
                print(f"[WIDGET] Update: {await response.json()} | {datetime.utcnow()}")

            other = Other.objects.get(id=1)
            params_two = {'access_token': STATUS_TOKEN,'text': f'Взломов: {digit_number(other.hacks)}👾 / Арестов {digit_number(other.arrest)}🔐','group_id': ID,'v': V}
            async with session.post(f"{API}/{METHOD_TWO}", params = params_two) as response:
                print(f"[STATUS] Update: {await response.json()} | {datetime.utcnow()}")      
        except Exception as ex:
        	print(f"Error: {ex} | {datetime.utcnow()}")

        await session.close()
        json_file.close()