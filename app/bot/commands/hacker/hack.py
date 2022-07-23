from app.bot import handler
from decimal import Decimal
from random import randint as random
from time import time, localtime, strftime
from app.models import Account, Hacker, Police, Hacks, Other, BotNet


@handler.message(name = 'взлом', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    hacker = Hacker.objects.get(user=user)
    text = f"{user()} "
    if time() >= hacker.arrest_time:
        if int(time()) - hacker.hack_time >= 0:
            count = Hacks.objects.count()
            hack = Hacks.objects.get(id=random(1, count))
            mention = random(1, 100) - (hacker.computer + hacker.mobile + hacker.programm) + (0 if int(time()) >= user.buffs_one_time else 10)
            botnet_money = (BotNet.objects.get(id=user.botnet_id).users_count * 100) if user.botnet_id != 0 else 0
            if mention > 20 and int(time()) >= user.buffs_three_time:
                ids = []
                count_police = random(1, 5)
                for police in Account.objects.filter(dialog = Account.Dialog.POLICE):
                    if random(0, 100) <= 50:
                        ids.append(police.user_id)
                    if len(ids) < count_police:
                        break
                if len(ids) > 0:
                    hacker.answer_id = random(0, 100000000)
                    for id in ids:
                        police_user = Account.objects.get(user_id=id)
                        msg.inline_buttons({"name": f"📟 Ответить {hacker.answer_id}"})
                        await msg(f"{police_user()} внимание, поступил вызов!\n{hack.mention}\n📟 Код вызова: {hacker.answer_id}", user_id = police_user.user_id)

            if Other.objects.get(id=1).holiday:
                holiday_gift = random(0, 1)
                if holiday_gift == 1:
                    gift_count = random(1, 10)
                    user.holiday_temp += gift_count
            user.balance += Decimal(((50 if int(time()) >= user.buffs_two_time else 75) * hacker.income_hack) + botnet_money)
            hacker.hack_time = time() + 300
            hacker.hacks_count += 1
            hacker.hacks_rating += 1
            Other.objects.filter(id=1).update(hacks = Other.objects.get(id=1).hacks + 1)
            hacker.save()
            user.save()
            text += f'{hack.text}, ваш доход со взлома: {user.digit_number(((50 if int(time()) >= user.buffs_two_time else 75) * hacker.income_hack) + botnet_money)} $'
            if Other.objects.get(id=1).holiday:
                if holiday_gift == 1:
                    text += f" и {gift_count} {user.decline(gift_count, ['подарок', 'подарка', 'подарков'])} 🎁"
            sticker = 20481
        else:
            text += f"вам нужно залечь на дно.\nСледующая попытка будет доступна через {str(strftime('%M мин.', localtime(hacker.hack_time - time()))).lstrip('0') if hacker.hack_time - time() > 60 else 'несколько секунд'}"
            sticker = 8471
    else:
        text += f"вы были арестованы, вы не сможете взламывать еще {str(strftime('%M мин.', localtime(hacker.arrest_time - time()))).lstrip('0') if hacker.arrest_time - time() > 60 else 'несколько секунд'}"
        sticker = 20463

    await msg(text)
    await msg(sticker_id=sticker)
    
@handler.message(name = 'заплатить штраф', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    hacker = Hacker.objects.get(user=user)
    if time() <= hacker.arrest_time:
        if (user.balance - hacker.escape_money) >= 0:
            user.balance -= Decimal(hacker.escape_money)
            hacker.arrest_time = 0
            hacker.save()
            user.save()
            text = f"{user()} вы заплатили штраф в размере {user.digit_number(int(hacker.escape_money))} $ {user.emoji()}"
        else:
            text = f"{user()} у вас не достаточно денег {user.emoji_bad()}"
    else:
        text = f"{user()} в данный момент вы не находитесь под арестом {user.emoji()}"

    await msg(text)