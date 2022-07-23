from app.bot import handler
from random import randint as random
from app.models import Account, Hacker, Police


keyboard_start = (
						{"name": "Хакер", "color": "negative"},
					  	{"name": "Полиция", "color": "primary"}
				)

keyboard_hacker = (
						{"name": "👾 Взлом", "color": "negative"},
						{"name": "💻 Ботнет", "color": "primary"},
				)
keyboard_hacker_two = (
						{"name": "🛒 Магазин", "color": "positive"}, 
						{"name": "📋 Профиль", "color": "secondary"},
						{"name": "💽 Ферма", "color": "secondary"}
					)
keyboard_hacker_three = (
						{"name": "📚 Помощь", "color": "positive"}
					)

keyboard_police = (
						{"name": "⚙ Работать", "color": "negative"},
						{"name": "👥 Команда", "color": "primary"},
					)

keyboard_police_two = (
						{"name": "🛒 Магазин", "color": "positive"}, 
						{"name": "📋 Профиль", "color": "secondary"}, 
						{"name": "📚 Помощь", "color": "positive"}
					)


@handler.message(name = '', dialog = Account.Dialog.START)
async def _(msg, user):
	text = f'{user()} добро пожаловать в Cloudlet Bot!'
	text += '\nКем ты хочешь стать?\nОтважным полицейским или злобным хакером?'
	text += f'\nВыбирай сторону, нажми на кнопку, все просто! {user.emoji()}'
	text += "\n(Если у тебя нету кнопок, напиши Хакер/Полиция)"
	user.dialog = Account.Dialog.DEFAULT
	user.save()

	msg.buttons(keyboard_start)

	await msg(text, attachment="photo-198059264_457239040")
	

@handler.message(name = 'хакер', dialog = Account.Dialog.DEFAULT)
async def _(msg, user):
	print("\t\t\n\n\t\t")
	text = f'{user()} Хороший выбор! {user.emoji()}'
	text += f'\nВзламывайте, попадайте в топы и старайтесь не попасть в руки полиции! {user.emoji()}'
	user.dialog = Account.Dialog.HACKER
	user.save()
	Hacker.objects.create(user=user)

	msg.buttons(keyboard_hacker)
	msg.buttons(keyboard_hacker_two)
	msg.buttons(keyboard_hacker_three)

	response = await msg(text)
	print(response)


@handler.message(name = 'полиция', dialog = Account.Dialog.DEFAULT)
async def _(msg, user):
	text = f'{user()} Хороший выбор! {user.emoji()}'
	text += '\nС каждым взломом вам будут приходить оповещения.\n'
	text += 'Отвечайте на сообщения быстрее, пока другой полицейский не ответил на него!'
	text += f'\nВы можете провалить поимку хакера, дабы избежать этого улучшайте предметы в магазине {user.emoji()}'
	user.dialog = Account.Dialog.POLICE
	user.save()
	Police.objects.create(user=user)

	msg.buttons(keyboard_police)
	msg.buttons(keyboard_police_two)

	await msg(text)