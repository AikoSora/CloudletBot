from decimal import Decimal
from app.bot import handler
from random import randint as random
from app.models import Account, Police, PoliceCommands


keyboard_default = (
						{"name": "⚙ Работать", "color": "negative"},
						{"name": "👥 Команда", "color": "primary"},
					)

keyboard_default_two = (
						{"name": "🛒 Магазин", "color": "positive"}, 
						{"name": "📋 Профиль", "color": "secondary"}, 
						{"name": "📚 Помощь", "color": "positive"}
					)

keyboard_create_or_cancel = (
								{'name': "Создать", "color": "positive"},
								{'name': "Отмена", "color": "negative"}
							)
def helpPC(user):
	text = f"{user()} помощь:"
	text += f"\n👥 Команда создать <Название> - создать команду"
	text += f'\n📲 Команда вступить <ID> <Пароль> - вступить в команду'
	text += f"\n📚 Команда помощь - помощь"
	text += f"\n\n💡 Команда повышает вашу удачу {user.emoji()}"
	return text

@handler.message(name='команда', dialog = Account.Dialog.POLICE, with_args=True)
async def _(msg, user):
	keyboard = 'keyboard_default'
	if len(msg.path_args) >= 3:
		if msg.path_args[1] == "создать":
			if len(msg.event['object']['message']['text'][15:].strip()) <= 10:
				if user.botnet_id == 0:
					police_luck = Police.objects.get(user=user)
					police_money = 500 * (police_luck.equipment + police_luck.transport)
					user.dialog = Account.Dialog.CREATE_PC
					user.temp = f"{msg.event['object']['message']['text'][15:].replace(',', '').strip()},{police_money}"
					temp = user.temp.strip().split(",")
					text = f"{user()} информация:"
					text += f"\n📋 Название: {temp[0]}"
					text += f'\n💳 Стоимость: {user.digit_number(int(temp[1]))}$'
					text += f"\n💡 Создать команду? 🙃"
					keyboard = 'keyboard_create_or_cancel'
				else:
					text = f"{user()} Вы уже состоите в команде {user.emoji_bad()}"
			else:
				text = f"{user()} Название команды не должно превышать 10 символов {user.emoji_bad()}"
		elif msg.path_args[1] == "вступить":
			if len(msg.path_args) >= 4:
				command = msg.path_args[2]
				try:
					if user.botnet_id == 0:
						command = PoliceCommands.objects.get(id = int(msg.path_args[2]))
						if msg.path_args[3] == str(command.password):
							users = command.users.replace(".", " ").strip().split()
							if len(users) < 5:
								users.append(f"{user.id}")
								command.users = ".".join(users)
								user.botnet_id = command.id
								command.save()
								text = f"{user()} Вы успешно присоеденились к команде {user.emoji()}"
							else:
								text = f"{user()} В команде закончились места {user.emoji_bad()}"
						else:
							text = f"{user()} Пароль не верный {user.emoji_bad()}"
					else:
						text = f"{user()} Вы уже состоите в команде {user.emoji_bad()}"
				except:
					text = f"{user()} Команда с таким ID не найдена {user.emoji_bad()}"
			else:
				text = f"{user()} Использование: Команда вступить <ID> <Пароль>"
		else:
			text = helpPC(user)
	elif len(msg.path_args) == 2:
		if msg.path_args[1] == "помощь":
			text = helpPC(user)
		else:
			text = helpPC(user)
	else:
		if user.botnet_id == 0:
			text = helpPC(user)
		else:
			command = PoliceCommands.objects.get(id=user.botnet_id)
			count = len(command.users.replace(".", " ").strip().split())
			text = f"{user()} информация:"
			text += f"\n🆔 ID Команды: {command.id}"
			text += f"\n📋 Название: {command.command_name}"
			text += f"\n👥 Участников: {count}/5"
			text += f"\n☘ Удача: +{count}"
			text += f"\n\n💡 Пароль для вступления: {command.password}"

	user.save()

	if keyboard == "keyboard_default":
		msg.buttons(keyboard_default)
		msg.buttons(keyboard_default_two)
	elif keyboard == "keyboard_create_or_cancel":
		msg.buttons(keyboard_create_or_cancel)

	await msg(text)

@handler.message(name = 'создать', dialog = Account.Dialog.CREATE_PC)
async def _(msg, user):
	temp = user.temp.strip().split(",")
	user.temp = ""
	user.dialog = Account.Dialog.POLICE
	if user.balance - int(temp[1]) >= 0:
		user.balance -= Decimal(int(temp[1]))
		command = PoliceCommands.objects.create(command_name = temp[0], users=f"{user.id}", password=f"{user.user_id}", id=(PoliceCommands.objects.count()+1))
		user.botnet_id = command.id
		text = f"{user()} Команда успешно создана {user.emoji()}"
	else:
		text = f"{user()} У вас не достаточно средств {user.emoji_bad()}"
	user.save()

	msg.buttons(keyboard_default)
	msg.buttons(keyboard_default_two)
	await msg(text)


@handler.message(name = 'отмена', dialog = Account.Dialog.CREATE_PC)
async def _(msg, user):
	user.temp = ""
	user.dialog = Account.Dialog.POLICE
	user.save()
	msg.buttons(keyboard_default)
	msg.buttons(keyboard_default_two)
	await msg(f"{user()} возврат в главное меню 🚀")