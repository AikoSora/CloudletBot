from app.bot import handler
from decimal import Decimal
from app.models import Account, Promo
from random import randint as random, choice as CH

random_text_for_nick = ["отличный ник", "чудесный ник", "замечательный ник"]

@handler.message(name = 'промо', with_args=True)
async def _(msg, user):
	if len(msg.path_args) >= 2:
		text = f"{user()} "
		try:
			promo = Promo.objects.get(name=msg.path_args[1])
			if user.old_activation_promo_id != promo.id:
				user.balance += Decimal(promo.price)
				user.old_activation_promo_id = promo.id
				user.save()
				promo.activated += 1
				promo.save()
				text += f"промокод успешно активирован, на ваш баланс зачислено {promo.price}$ {user.emoji()}"
				if promo.activated == promo.max_users:
					Promo.objects.filter(id=promo.id).delete()
			else:
				text += f"вы уже активировали данный промокод {user.emoji_bad()}"
		except:
			text += f"такой акции нет или она была уже завершена {user.emoji_bad()}\nСледите за новостями нашей группы чтобы первым использовать промокоды! {user.emoji()}"
		await msg(text)
	else:
		await msg(f"{user()} следите за новостями нашей группы чтобы первым использовать промокоды! {user.emoji()}")

@handler.message(name = 'ник', with_args=True)
async def _(msg, user):
	if len(msg.path_args) >= 2:
		if len(msg.path_args[1]) <= 10:
			user_nick = msg.event['object']['message']['text'].split()
			user.username = user_nick[1].replace("$", "?")
			user.save()
			text = f"{user()} "
			text += CH(random_text_for_nick)
			text += f" {user.emoji()}"
		else:
			text = f"{user()} "
			text += f"длина ника не должна превышать 10 символов {user.emoji_bad()}"

		await msg(text)
	else:
		await msg(f"{user()} использование: ник <ник> {user.emoji_bad()}")
