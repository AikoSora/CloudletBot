from time import time
from datetime import datetime
from app.bot import handler
from random import randint as random
from app.models import Account, Hacker, Police, PoliceCommands, Other

emoji_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
emoji_top = ['1⃣ ','2⃣','3⃣ ','4⃣','5⃣','6⃣','7⃣ ','8⃣','9⃣','🔟','1⃣1⃣', '1⃣2⃣', '1⃣3⃣', '1⃣4⃣', '1⃣5⃣']

async def mailall(msg, user):
        if len(msg.path_args) >= 4:
            wall = msg.path_args[1]
            message = msg.event['object']['message']['text'].split()
            message = ' '.join(x for x in message[3:])
            hacker_or_police = msg.path_args[2]
            text = f"{user()} "
            if hacker_or_police == "hacker":
                hor = Account.Dialog.HACKER
            elif hacker_or_police == "police":
                hor = Account.Dialog.POLICE

            users_id = [[]]
            for human in Account.objects.filter(dialog=hor, mention=0).all():
                if len(users_id[len(users_id)-1]) < 100:
                    users_id[len(users_id)-1].append(str(human.user_id))
                else:
                    users_id.append([str(human.user_id)])

            for user_array in users_id:
                await msg(message, attachment = wall, user_ids = ",".join(user_array))
            
            await msg("Рассылка закончена.")
        else:
            await msg("mailall <wall><owner_id>_<media> <Hacker or Police> <message>")

@handler.message(name = 'mailall', with_args=True)
async def _(msg, user):
    if user.user_id == 338845100:
        await mailall(msg, user)

@handler.message(name = 'репорт', with_args=True)
async def _(msg, user):
    if len(msg.path_args) >= 2:
        if time() >= user.report_time:
            report_text = f"{Account.objects.get(user_id=338845100).username}, входящий репорт!\nПользователь: [id{user.user_id}|{user.username}]\nID в боте: {user.id}"
            text = f"{user()} спасибо, Мы уже работаем над вашей заявкой {user.emoji()}"
            sticker = 50900

            await Account.TempBot.api("messages.send", {"user_id": 338845100,
                                        "message": report_text,
                                        "forward_messages": msg.event['object']['message']['id'],
                                        "random_id": random(0, 100000000)})

            user.report_time = time() + 300
            user.save()
        else:
            text = f"{user()} попробуйте отправить еще один репорт - немного позже {user.emoji()}"
            sticker = 50876

        await msg(text)
        await msg(sticker_id = sticker)
    else:
        await msg(f"{user()} использование: репорт <жалоба> (вложения)")

async def holiday(msg, user):
    if user.user_id == 338845100:
        if len(msg.path_args) >= 2:
            if msg.path_args[1] == "start":
                Other.objects.filter(id=1).update(holiday=True)
                await msg(f"{user()} Holiday started")
            elif msg.path_args[1] == "stop":
                Other.objects.filter(id=1).update(holiday=False)
                await msg(f"{user()} Holiday stoped")
            else:
                await msg(f"{user()} использование: holiday [start/stop]")
        else:
            await msg(f"{user()} использование: holiday [start/stop]")


@handler.message(name = 'holiday', dialog = Account.Dialog.POLICE, with_args=True)
async def _(msg, user):
    await holiday(msg, user)


async def holiday_top(msg, user):
    if user.user_id == 338845100:
        text = "Top\n"
        for i, human in enumerate(Account.objects.all().order_by('-holiday_temp')[:15]):
            username = f"[id{human.user_id}|{human.username}]" if human.user_id != user.user_id else "Вы"
            text += f'\n{emoji_top[i]} {username} - {user.digit_number(human.holiday_temp)} 🎁'
        await msg(text)

@handler.message(name = 'holiday_top')
async def _(msg, user):
    await holiday_top(msg, user)

@handler.message(name = "last_message")
async def _(msg, user):
    if user.user_id == 338845100:
        last_message_time = Account.objects.all().order_by("message_time")[0]
        time_message = datetime.utcfromtimestamp(last_message_time.message_time).strftime("%H:%M.%S")
        await msg(f"last message = {last_message_time} : {time_message}")