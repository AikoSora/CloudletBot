from django.core.management import BaseCommand
from django.conf import settings
from app.models import *
from json import dumps
from time import *
from random import randint as random
import os, uvloop, asyncio, aiohttp

TOKEN = "ABOBA"
GROUP_ID = 198059264
V = '5.120'
API = 'https://api.vk.com/method/messages.send'
keyboard_start = dumps({"one_time": False, "buttons": [[{"action": {"type": "text", "label": "Хакер"}, "color": "negative"},{"action": {"type": "text", "label": "Полиция"}, "color": "primary"}]]})

class Command(BaseCommand):
	def handle(self, *args, **options):
		os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
		uvloop.install()
		self.ioloop = asyncio.get_event_loop() 
		self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.vape())]))
		self.ioloop.close()

	async def vape(self):
		os.system("supervisorctl stop cloudletbot")
		os.system("supervisorctl stop widget")

		count = 15
		for i, hacker in enumerate(Hacker.objects.all().order_by('-hacks_count')[:15]):
			user = Account.objects.get(user_id=hacker.user.user_id)
			user.donate_points += count
			user.save()
			count -= 1
			
		count = 15
		for i, police in enumerate(Police.objects.all().order_by('-arrest_count')[:15]):
			user = Account.objects.get(user_id=police.user.user_id)
			user.donate_points += count
			user.save()
			count -= 1

		Account.objects.all().update(dialog=Account.Dialog.DEFAULT, balance=0, temp="", botnet_id=0, report_time=0)
		Hacker.objects.all().delete()
		Police.objects.all().delete()
		BotNet.objects.all().delete()
		PoliceCommands.objects.all().delete()
		Other.objects.filter(id=1).update(hacks=0, arrest=0)

		session = aiohttp.ClientSession()

		users_id = [[]]
		for human in Account.objects.all():
			if len(users_id[len(users_id)-1]) < 100:
				users_id[len(users_id)-1].append(str(human.user_id))
			else:
				users_id.append([str(human.user_id)])

		os.system("supervisorctl start cloudletbot")
		os.system("supervisorctl start widget")

		for user_array in users_id:
			params={"user_ids": ",".join(user_array),
					"message": "А вот и вайп, кем ты хочешь стать на этот раз?\nВыбирай сторону! 😉",
					"attachment": "photo-198059264_457239260",
					"keyboard": keyboard_start,
					"random_id": random(0, 10000000)}

			params.update({'access_token': TOKEN, 'group_id': GROUP_ID, 'v': V})
			async with session.post(f"{API}", params = params) as response:
				print(await response.json())

		await session.close()
