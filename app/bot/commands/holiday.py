from app.bot import handler
from random import randint as random
from app.models import Account, Other
from time import time, localtime, strftime

emoji_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '0']
emoji_top = ['1⃣ ','2⃣','3⃣ ','4⃣','5⃣','6⃣','7⃣ ','8⃣','9⃣','🔟','0️⃣']
keyboard_holiday = {"name": "👑 Топ"}

@handler.message(name = 'подарки')
async def _(msg, user):
	if Other.objects.get(id=1).holiday:
		text = f"{user()} "
		if time() >= user.holiday_time:
			gift_count = random(10, 20)
			user.holiday_temp += gift_count
			user.holiday_time = time() + 300
			user.save()
			text += f"Вы получили {gift_count} {user.decline(gift_count, ['подарок', 'подарка', 'подарков'])} 🎁"
		else:
			text += f"Ваши подарки еще не готовы, вернитесь за ними через {str(strftime('%M мин.', localtime(user.holiday_time - time()))).lstrip('0') if user.holiday_time - time() > 60 else 'несколько секунд'} {user.emoji_bad()}"
		await msg(text)

@handler.message(name = 'новогодний', with_args=True)
async def _(msg, user):
	if Other.objects.get(id=1).holiday:
		text = f"{user()} новогодний топ:"
		for i, human in enumerate(Account.objects.all().order_by('-holiday_temp')[:10]):
			text += f'\n{emoji_top[i]} {human(True) if human.user_id != user.user_id else "Вы"} - {user.digit_number(human.holiday_temp)} 🎁'

		text += '\n————————————————'

		for i, human in enumerate(Account.objects.all().order_by('-holiday_temp')):
			if user.user_id == human.user_id and i >= 10 and i < 1000:
				count_in_top = list(str(i+1))

				for count, letter in enumerate(count_in_top):
					for enum, emoji in enumerate(emoji_count):
						if letter == emoji:
							count_in_top[count] = emoji_top[enum]
							break

				count_in_top = ''.join(x for x in count_in_top)
				text += f'\n{count_in_top} - {human(True)} - {user.digit_number(user.holiday_temp)} 🎁'
				break
			elif user.user_id == human.user_id and i < 10:
				text += f"\n🔝 - Вы - {user.digit_number(user.holiday_temp)} 🎁"
				break
			elif i == 1000:
				text += f'\n▶1&#8419;0&#8419;0&#8419;0&#8419; - {user(True)} - {user.digit_number(user.holiday_temp)} 🎁'
				break
		msg.inline_buttons(keyboard_holiday)
		await msg(text)
