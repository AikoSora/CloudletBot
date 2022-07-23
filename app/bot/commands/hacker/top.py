from app.bot import handler
from random import randint as random
from app.models import Account, Hacker, Other

emoji_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '0']
emoji_top = ['1⃣ ','2⃣','3⃣ ','4⃣','5⃣','6⃣','7⃣ ','8⃣','9⃣','🔟','0️⃣']

@handler.message(name = 'топ', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    text = f'{user()} топ хакеров:'
    userintop = False

    for i, hacker in enumerate(Hacker.objects.all().order_by('-hacks_count')[:1000]):
        if i < 10:
            if user.user_id == hacker.user.user_id:
                userintop = True
            text += f'\n{emoji_top[i]} {hacker.user(True) if hacker.user.user_id != user.user_id else "Вы"} - {user.digit_number(hacker.hacks_count)} 👑'
        else:
            if userintop:
                text += '\n————————————————'
                text += f"\n🔝 - Вы - {user.digit_number(Hacker.objects.get(user=user).hacks_count)} 👑"
                break
            elif user.user_id == hacker.user.user_id and i < 1000:
                text += '\n————————————————'
                count_in_top = list(str(i+1))
                for count, letter in enumerate(count_in_top):
                    for enum, emoji in enumerate(emoji_count):
                        if letter == emoji:
                            count_in_top[count] = emoji_top[enum]
                            break
                count_in_top = ''.join(x for x in count_in_top)
                text += f'\n{count_in_top} - {hacker.user(True)} - {user.digit_number(hacker.hacks_count)} 👑'
                break
    else:
        text += f'\n▶1&#8419;0&#8419;0&#8419;0&#8419; - {user(True)} - {user.digit_number(Hacker.objects.get(user=user).hacks_count)} 👑'

    if Other.objects.get(id=1).holiday:
        msg.inline_buttons({"name": "🎁 Новогодний"})

    await msg(text)
