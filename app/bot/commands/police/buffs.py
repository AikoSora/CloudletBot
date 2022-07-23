from app.bot import handler
from random import randint as random
from app.models import Account, Police
from time import time, localtime, strftime


@handler.message(name = 'усиления', dialog = Account.Dialog.POLICE)
async def _(msg, user):
	text = f'{user()} усиления:'
	text += "\n☘ Повышенная удача:"
	text += "\n&#12288;💡 Описание: повышает удачу на 1ч"
	text += '\n&#12288;💸 Стоимость: 10Б' if int(time()) >= user.buffs_one_time else f"\n&#12288;⌛ Оставшееся время: {str(strftime('%M мин.', localtime(user.buffs_one_time - time()))).lstrip('0') if user.buffs_one_time - time() > 60 else 'несколько секунд'}"
	text += "\n\n💰 Повышенный заработок:"
	text += "\n&#12288;💡 Описание: повышает заработок на 1ч"
	text += "\n&#12288;💸 Стоимость: 15Б" if int(time()) >= user.buffs_two_time else f"\n&#12288;⌛ Оставшееся время: {str(strftime('%M мин.', localtime(user.buffs_two_time - time()))).lstrip('0') if user.buffs_two_time - time() > 60 else 'несколько секунд'}"
	text += "\n\n🍀 Без штрафов:"
	text += "\n&#12288;💡 Описание: Убирает штрафы за провал поимки хакера на 5ч"
	text += "\n&#12288;💸 Стоимость: 20Б" if int(time()) >= user.buffs_three_time else f"\n&#12288;⌛ Оставшееся время: {str(strftime('%H ч. %M мин.', localtime(user.buffs_three_time - time()))).lstrip('0') if user.buffs_three_time - time() > 60 else 'несколько секунд'}"
	text += f"\n\n💸 Баланс: {user.digit_number(int(user.donate_points))}Б"

	keyboard = []
	keyboard_two = []

	if int(time()) >= user.buffs_one_time:
		keyboard.append({"name": "⭐ Усиление 1"})

	if int(time()) >= user.buffs_two_time:
		keyboard.append({"name": "⭐ Усиление 2"})

	if int(time()) >= user.buffs_three_time:
		if len(keyboard) < 2:
			keyboard.append({"name": "⭐ Усиление 3"})
		else:
			keyboard_two.append({"name": "⭐ Усиление 3"})

	if len(keyboard) > 0:
		msg.inline_buttons(keyboard)

	if len(keyboard_two) > 0:
		msg.inline_buttons(keyboard_two)

	await msg(text)


@handler.message(name = 'усиление', dialog = Account.Dialog.POLICE, with_args=True)
async def _(msg, user):
	text = f"{user()} "
	if len(msg.path_args) >= 2:
		if msg.path_args[1] == "1":
			if int(time()) >= user.buffs_one_time:
				if user.donate_points - 10 >= 0:
					user.donate_points -= 10
					user.buffs_one_time = int(time()) + 3600
					user.save()
					text += f"вы успешно приобрели усиление 'Повышенная удача' за 10Б {user.emoji()}"
				else:
					text += f"у вас не достаточно баллов {user.emoji_bad()}"
			else:
				text += f"у вас уже есть данное усиление {user.emoji_bad()}"
		elif msg.path_args[1] == "2":
			if int(time()) >= user.buffs_two_time:
				if user.donate_points - 15 >= 0:
					user.donate_points -= 15
					user.buffs_two_time = int(time()) + 3600
					user.save()
					text += f"вы успешно приобрели усиление 'Повышенный заработок' за 15Б {user.emoji()}"
				else:
					text += f"у вас не достаточно баллов {user.emoji_bad()}"
			else:
				text += f"у вас уже есть данное усиление {user.emoji_bad()}"
		elif msg.path_args[1] == "3":
			if int(time()) >= user.buffs_three_time:
				if user.donate_points - 20 >= 0:
					user.donate_points -= 20
					user.buffs_three_time = int(time()) + 18000
					user.save()
					text += f"вы успешно приобрели усиление 'Без штрафов' за 20Б {user.emoji()}"
				else:
					text += f"у вас не достаточно баллов {user.emoji_bad()}"
			else:
				text += f"у вас уже есть данное усиление {user.emoji_bad()}"
		else:
			text += f"использование: Усиление <номер> {user.emoji_bad()}"
	else:
		text += f"использование: Усиление <номер> {user.emoji_bad()}"

	await msg(text)


@handler.message(name = 'усиления', dialog = Account.Dialog.HACKER)
async def _(msg, user):
	text = f'{user()} усиления:'
	text += "\n☘ Повышенная анонимность:"
	text += "\n&#12288;💡Описание: повышает анонимность на 1ч"
	text += '\n&#12288;💸 Стоимость: 10Б' if int(time()) >= user.buffs_one_time else f"\n&#12288;⌛ Оставшееся время: {str(strftime('%M мин.', localtime(user.buffs_one_time - time()))).lstrip('0') if user.buffs_one_time - time() > 60 else 'несколько секунд'}"
	text += "\n\n💰 Повышенный заработок:"
	text += "\n&#12288;💡Описание: повышает заработок на 1ч"
	text += "\n&#12288;💸 Стоимость: 15Б" if int(time()) >= user.buffs_two_time else f"\n&#12288;⌛ Оставшееся время: {str(strftime('%M мин.', localtime(user.buffs_two_time - time()))).lstrip('0') if user.buffs_two_time - time() > 60 else 'несколько секунд'}"
	text += "\n\n🍀 Без арестов:"
	text += "\n&#12288;💡Описание: Убирает аресты за провал взлома на 1ч"
	text += "\n&#12288;💸 Стоимость: 20Б" if int(time()) >= user.buffs_three_time else f"\n&#12288;⌛ Оставшееся время: {str(strftime('%M мин.', localtime(user.buffs_three_time - time()))).lstrip('0') if user.buffs_three_time - time() > 60 else 'несколько секунд'}"
	text += f"\n\n💸 Баланс: {user.digit_number(int(user.donate_points))}Б"

	keyboard = []
	keyboard_two = []

	if int(time()) >= user.buffs_one_time:
		keyboard.append({"name": "⭐ Усиление 1"})

	if int(time()) >= user.buffs_two_time:
		keyboard.append({"name": "⭐ Усиление 2"})

	if int(time()) >= user.buffs_three_time:
		if len(keyboard) < 2:
			keyboard.append({"name": "⭐ Усиление 3"})
		else:
			keyboard_two.append({"name": "⭐ Усиление 3"})

	if len(keyboard) > 0:
		msg.inline_buttons(keyboard)

	if len(keyboard_two) > 0:
		msg.inline_buttons(keyboard_two)

	await msg(text)

@handler.message(name = 'усиление', dialog = Account.Dialog.HACKER, with_args=True)
async def _(msg, user):
	text = f"{user()} "
	if len(msg.path_args) >= 2:
		if msg.path_args[1] == "1":
			if int(time()) >= user.buffs_one_time:
				if user.donate_points - 10 >= 0:
					user.donate_points -= 10
					user.buffs_one_time = int(time()) + 3600
					user.save()
					text += f"вы успешно приобрели усиление 'Повышенная анонимность' за 10Б {user.emoji()}"
				else:
					text += f"у вас не достаточно баллов {user.emoji_bad()}"
			else:
				text += f"у вас уже есть данное усиление {user.emoji_bad()}"
		elif msg.path_args[1] == "2":
			if int(time()) >= user.buffs_two_time:
				if user.donate_points - 15 >= 0:
					user.donate_points -= 15
					user.buffs_two_time = int(time()) + 3600
					user.save()
					text += f"вы успешно приобрели усиление 'Повышенный заработок' за 15Б {user.emoji()}"
				else:
					text += f"у вас не достаточно баллов {user.emoji_bad()}"
			else:
				text += f"у вас уже есть данное усиление {user.emoji_bad()}"
		elif msg.path_args[1] == "3":
			if int(time()) >= user.buffs_three_time:
				if user.donate_points - 20 >= 0:
					user.donate_points -= 20
					user.buffs_three_time = int(time()) + 3600
					user.save()
					text += f"вы успешно приобрели усиление 'Без арестов' за 20Б {user.emoji()}"
				else:
					text += f"у вас не достаточно баллов {user.emoji_bad()}"
			else:
				text += f"у вас уже есть данное усиление {user.emoji_bad()}"
		else:
			text += f"использование: Усиление <номер> {user.emoji_bad()}"
	else:
		text += f"использование: Усиление <номер> {user.emoji_bad()}"

	await msg(text)

