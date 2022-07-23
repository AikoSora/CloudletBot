from time import time
from app.bot import handler
from decimal import Decimal
from random import randint as random
from app.models import Account, Police, Hacker, Other, PoliceSystemCall, PoliceCommands

keyboard = {"name": "💰 Заплатить штраф"}

@handler.message(name = 'ответить', dialog = Account.Dialog.POLICE, with_args=True)
async def _(msg, user):
    if len(msg.path_args) >= 2:
        if msg.path_args[1].isdigit():
            police = Police.objects.get(user=user)
            text = f'{user()} '
            call_id = int(msg.path_args[1]) if int(msg.path_args[1]) != 0 else 1
            not_PSK = True
            luck = 0
            try:
                try:
                    hacker = Hacker.objects.get(answer_id=call_id)
                except:
                    hacker = PoliceSystemCall.objects.get(answer_call_id = call_id)
                    not_PSK = False
                if user.botnet_id != 0:
                    luck = len(PoliceCommands.objects.get(id = user.botnet_id).users.replace(".", "").strip().split())
                if (random(0, 100) - (police.equipment + police.transport + luck)) <= 50:
                    money = 2000 * ((police.equipment + police.transport) + (0 if int(time()) >= user.buffs_two_time else 10))
                    user.balance += Decimal(money)
                    if Other.objects.get(id=1).holiday:
                        holiday_gift = random(0, 1)
                        if holiday_gift == 1:
                            gift_count = random(1, 10)
                            user.holiday_temp += gift_count
                    text += f'вы успешно арестовали хакера, ваша награда: {user.digit_number(money)} $'
                    if Other.objects.get(id=1).holiday:
                        if holiday_gift == 1:
                            text += f" и {gift_count} {user.decline(gift_count, ['подарок', 'подарка', 'подарков'])} 🎁"
                    if not_PSK:
                        hacker.hacks_count -= 1 if hacker.hacks_count > 0 else 0
                        if hacker.user_id != 585022835:
                            hacker.arrest_time = time() + 1800
                        hacker.answer_id = 0
                        hacker.escape_money = hacker.user.balance / 2 if hacker.user.balance > 100 else 75
                        Other.objects.filter(id=1).update(arrest = Other.objects.get(id=1).arrest + 1)
                        msg.inline_buttons(keyboard)

                        await msg(f"{hacker.user()} вы были пойманы за недавний взлом, ваш арест продлиться 30 минут.\
                            \nИли заплатите штраф в размере {user.digit_number(int(hacker.escape_money))} $ {user.emoji()}",
                            user_id = hacker.user.user_id)
                    else:
                        hacker.answer_call_id = 0
                        Other.objects.filter(id=1).update(arrest = Other.objects.get(id=1).arrest + 1)
                    police.arrest_count +=1
                    police.arrest_rating +=1
                    await msg(text)
                else:
                    text += f'вам не удалось поймать хакера {user.emoji_bad()}'
                    money = int((user.balance * 15) / 100)
                    if user.balance - money >= 0 and int(time()) >= user.buffs_three_time:
                        text += f'\nВам был выписан штраф в размере {user.digit_number(money)} $'
                        user.balance -= Decimal(money)
                    police.arrest_count -= 1 if police.arrest_count > 0 else 0
                    if not_PSK:
                        hacker.answer_id = 0
                    else:
                        hacker.answer_call_id = 0
                    await msg(text)
                hacker.save()
                police.save()
                user.save()
            except:
                text += f'упс..\nКажется вы не успели ответить на вызов или такого вызова нету, ждите еще {user.emoji()}'
                await msg(text)
