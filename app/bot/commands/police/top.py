from app.bot import handler
from random import randint as random
from app.models import Account, Police, Other

emoji_count = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '0']
emoji_top = ['1⃣ ','2⃣','3⃣ ','4⃣','5⃣','6⃣','7⃣ ','8⃣','9⃣','🔟','0️⃣']

keyboard_holiday = {"name": "🎁 Новогодний"}

@handler.message(name = 'топ', dialog = Account.Dialog.POLICE)
async def _(msg, user):
    text = f'{user()} топ полицейских:'

    for i, police in enumerate(Police.objects.all().order_by('-arrest_count')[:10]):
        text += f'\n{emoji_top[i]} {police.user(True) if police.user.user_id != user.user_id else "Вы"} - {user.digit_number(police.arrest_count)} 👑'

    text += '\n————————————————'

    for i, police in enumerate(Police.objects.all().order_by('-arrest_count')):
        if user.user_id == police.user.user_id and i >= 10 and i < 1000:
            count_in_top = list(str(i+1))

            for count, letter in enumerate(count_in_top):
                for enum, emoji in enumerate(emoji_count):
                    if letter == emoji:
                        count_in_top[count] = emoji_top[enum]
                        break

            count_in_top = ''.join(x for x in count_in_top)
            text += f'\n{count_in_top} - {police.user(True)} - {user.digit_number(police.arrest_count)} 👑'
            break
        elif user.user_id == police.user.user_id and i < 10:
        	text += f"\n🔝 - Вы - {user.digit_number(Police.objects.get(user=user).arrest_count)} 👑"
        	break
        elif i == 1000:
            text += f'\n▶1&#8419;0&#8419;0&#8419;0&#8419; - {user(True)} - {user.digit_number(Police.objects.get(user=user).arrest_count)} 👑'
            break

    if Other.objects.get(id=1).holiday:
        msg.inline_buttons(keyboard_holiday)

    await msg(text)