from app.bot import handler
from decimal import Decimal
from random import randint as random
from app.models import Account, Hacker, BotNet

keyboard_default = (
						{"name": "👾 Взлом", "color": "negative"},
						{"name": "💻 Ботнет", "color": "primary"}
					)
keyboard_default_two = (
						{"name": "🛒 Магазин", "color": "positive"},
						{"name": "📋 Профиль", "color": "secondary"},
						{"name": "💽 Ферма", "color": "secondary"}
					)

keyboard_default_three = (
						{"name": "📚 Помощь", "color": "positive"},
					)

keyboard_create_or_cancel = (
								{"name": "Создать", "color": "positive"},
								{"name": "Отмена", "color": "negative"}
							)
def helpBotNet(user):
	text = f"[Cloudlet BotNet] Информация:"
	text += f"\n📚 Ботнет -h ▶ Помощь "
	text += f"\n💻 Ботнет -n <Name> ▶ Создать ботнет "
	text += f'\n\n💡 Ботнет сеть увеличивает заработок со взломов {user.emoji()}'
	return text

@handler.message(name = 'ботнет', dialog = Account.Dialog.HACKER, with_args=True)
async def _(msg, user):
	await msg("[Cloudlet BotNet] Загрузка..")

	keyboard = 'keyboard_default'
	if user.user_id != 58502283500:
		if len(msg.path_args) >= 3:
			if msg.path_args[1] == "-c":
				if user.botnet_id == 0:
					try:
						botnet = BotNet.objects.get(id=msg.path_args[2])
						if botnet.users_count < 15:
							user.botnet_id = botnet.id
							botnet.users_count += 1
							user.save()
							botnet.save()
							text = f"[Cloudlet BotNet] Вы подключены к ботнет сети {user.emoji()}"
						else:
							text = f"[Cloudlet BotNet] Сеть переполнена {user.emoji_bad()}"
					except:
						text = f"[Cloudlet BotNet] Cеть не найдена {user.emoji_bad()}"
				else:
					text = f"[Cloudlet BotNet] Вы уже подключены к сети {user.emoji_bad()}"
			elif msg.path_args[1] == "-n":
				if user.botnet_id == 0:
					if len(msg.event['object']['message']['text'][9:].strip()) <= 10:
						hack_account = Hacker.objects.get(user=user)
						user.dialog = Account.Dialog.CREATE_BN
						user.temp = f"{msg.event['object']['message']['text'][9:].replace(',', '').strip()},{500*(hack_account.programm + hack_account.computer + hack_account.mobile)}"
						temp = user.temp.strip().split(",")
						text = f"[Cloudlet BotNet] Информация:"
						text += f"\n📋 Название: {temp[0]}"
						text += f"\n💳 Стоимость: {user.digit_number(int(temp[1]))}$"
						text += f"\n💡 Создать ботнет сеть? 🙃"
						keyboard = 'keyboard_create_or_cancel'
					else:
						text = f"[Cloudlet BotNet] Длина названия не должна превышать 10 символов {user.emoji_bad()}"
				else:
					text = f"[Cloudlet BotNet] У вас уже есть ботнет сеть {user.emoji_bad()}"
			else:
				text = f"[Cloudlet BotNet] Kоманда не найдена {user.emoji_bad()}"
		else:
			if len(msg.path_args) >= 2:
				if msg.path_args[1] == "-h":
					text = helpBotNet(user)
				else:
					text = f"[Cloudlet BotNet] Kоманда не найдена {user.emoji_bad()}"
			else:
				if user.botnet_id == 0:
					text = helpBotNet(user)
				else:
					botnet = BotNet.objects.get(id=user.botnet_id)
					text = "[Cloudlet BotNet] Информация:"
					text += f"\n🆔 Ботнет ID: {botnet.id}"
					text += f"\n📋 Название: {botnet.botnet_name}"
					text += f"\n💳 Заработок: {botnet.users_count * 100}$"
					text += f"\n📈 Мощность: {botnet.users_count}БНр/15БНр"
					text += f'\n\n💡 Чтобы повысить мощность, попросите\n\
					другого хакера ввести "Ботнет -c {botnet.id}" {user.emoji()}' if botnet.users_count < 15 else ""
		user.save()

		if keyboard == "keyboard_default":
			msg.buttons(keyboard_default)
			msg.buttons(keyboard_default_two)
			msg.buttons(keyboard_default_three)
		elif keyboard == "keyboard_create_or_cancel":
			msg.buttons(keyboard_create_or_cancel)
			
		await msg(text)

@handler.message(name = 'создать', dialog = Account.Dialog.CREATE_BN, with_args=True)
async def _(msg, user):
	temp = user.temp.strip().split(",")
	user.temp = ""
	user.dialog = Account.Dialog.HACKER
	if user.balance - int(temp[1]) >= 0:
		user.balance -= Decimal(int(temp[1]))
		botnet = BotNet.objects.create(botnet_name=temp[0], users_count=1, id=(BotNet.objects.count()+1))
		user.botnet_id = botnet.id

		text = f"[Cloudlet BotNet] Ботнет сеть успешно создана {user.emoji()}"
	else:
		text = f"[Cloudlet BotNet] Не достаточно средств {user.emoji_bad()}"
	user.save()
	msg.buttons(keyboard_default)
	msg.buttons(keyboard_default_two)
	msg.buttons(keyboard_default_three)
	await msg(text)

@handler.message(name = 'отмена', dialog = Account.Dialog.CREATE_BN, with_args=True)
async def _(msg, user):
	user.temp = ""
	user.dialog = Account.Dialog.HACKER
	user.save()
	msg.buttons(keyboard_default)
	msg.buttons(keyboard_default_two)
	msg.buttons(keyboard_default_three)
	await msg("[Cloudlet BotNet] Отмена...")
