from decimal import Decimal
from app.bot import handler
from random import randint as random
from time import time, strftime, localtime
from app.models import Account, Police, WorkForPolice as WFP, Other


@handler.message(name = 'работать', dialog = Account.Dialog.POLICE)
async def _(msg, user):
    text = f"{user()} "
    police = Police.objects.get(user=user)
    if time() >= police.work_time:
        count = WFP.objects.count()
        work = WFP.objects.get(id=random(1, count)).text
        money = random(100, 1000) * ((police.equipment + police.transport) + (0 if int(time()) >= user.buffs_two_time else 10))
        text += f'{work}\nСегодня вы заработали: {user.digit_number(money)} $ {user.emoji()}'
        if Other.objects.get(id=1).holiday:
            holiday_gift = random(0, 1)
            if holiday_gift == 1:
                gift_count = random(1, 10)
                user.holiday_temp += gift_count
                text += f"\nПолучено {gift_count} {user.decline(gift_count, ['подарок', 'подарка', 'подарков'])} 🎁"
        police.work_time = time() + 300
        user.balance += Decimal(money)
        police.save()
        user.save()
        sticker = 20467
    else:
        text += f"вы слишком устали {user.emoji_bad()}\nСледующая попытка будет доступна через {str(strftime('%M мин.', localtime(police.work_time - time()))).replace('0', '') if police.work_time - time() > 60 else 'несколько секунд'}."
        sticker = 20463

    await msg(text)
    await msg(sticker_id = sticker)
