from django.core.management import BaseCommand
from django.conf import settings
from app.models import Account, Hacks, Police, PoliceSystemCall as PSC
import os, uvloop, asyncio, aiohttp, random, json, requests # requests мы юзаем ибо нам не нужен асинхрон в методе users.get


class Command(BaseCommand):

    session = None
    user_ids = []

    def handle(self, *args, **options):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.ioloop = asyncio.get_event_loop()
        self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.job())]))
        self.ioloop.close()

    async def job(self):
        self.session = aiohttp.ClientSession()
        print("[System Police Call] Mailing...")
        for users in Account.objects.filter(dialog=Account.Dialog.POLICE).all(): # смотрим кто онлайн и добавляем их в массив
            params = {"access_token": settings.BOT_TOKEN, "group_id": settings.BOT_GROUP_ID, "v": "5.103", "user_ids": users.user_id, "fields": "online"}
            response = requests.get("https://api.vk.com/method/users.get", params=params).json()
            if response['response'][0]['online'] == 1:
                self.user_ids.append(users.user_id)
    
        random_hacks = Hacks.objects.get(id=random.randint(1, Hacks.objects.count())) # получаем рандомное уведомление
        answer_id = random.randint(1, 100000000)
        PSC.objects.filter(id=1).update(answer_call_id = answer_id) # Регестрируем вызов
    
        for enum, users in enumerate(self.user_ids): # делаем рассылку о вызове
            if enum == 5:
                break
            user = Account.objects.get(user_id=users)
            params = {"access_token": settings.BOT_TOKEN, "group_id": settings.BOT_GROUP_ID, "v": "5.103",
                      "user_id": users, 
                      "message": f"{user(True)} внимание, поступил вызов!\n{random_hacks.mention}\n📟 Код вызова: {answer_id}",
                      "keyboard": json.dumps({"inline": True, "buttons": [[{"action": {"type": "text", "label": f"📟 Ответить {answer_id}"}, "color": "secondary"}]]}),
                      "random_id": random.randint(0, 100000000)}
            async with self.session.post("https://api.vk.com/method/messages.send", params = params) as response:
                print(f"[System Police Call] Message send {users}: {await response.json()}")
    
        self.user_ids = []
        await self.session.close()
        print("[System Police Call] Goodbay!")
