from decimal import Decimal
from app.bot import handler
from random import randint as random
from app.models import Account, Hacker

@handler.message(name = 'магазин', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    computer = user.hacker.get(user=user).computer
    programm = user.hacker.get(user=user).programm
    mobile = user.hacker.get(user=user).mobile
    text = f'{user()} улучшения:\n'
    text += f'\n💻 Компьютер: \n&#12288;⭐ Уровень {computer}' + (f'\n&#12288;💳 Стоимость: {user.digit_number(400 * computer)} $\n' if computer != 20 else "\n&#12288;💡 Максимально улучшен.\n")
    text += f'\n💿 Программное обеспечение:\n&#12288;⭐ Уровень {programm}' + (f'\n&#12288;💳 Стоимость: {user.digit_number(350 * programm)} $\n' if programm != 20 else "\n&#12288;💡 Максимально улучшено.\n")
    text += f'\n📱 Телефон:\n&#12288;⭐ Уровень {mobile}' + (f'\n&#12288;💳 Стоимость: {user.digit_number(200 * mobile)} $\n' if mobile != 20 else "\n&#12288;💡 Максимально улучшен.\n")
    text += f"\n💳 Баланс: {user.digit_number(user.balance) if user.balance != 0.00000000 else 0.00000000}$"
    text += f'\n\n💡 Улучшая данные предметы, вы увеличиваете свою анонимность и заработок {user.emoji()}'

    keyboard = []

    if computer + programm < 40:
        if computer < 20:
            keyboard.append({"name": "💻 Компьютер"})
        if programm < 20:
            keyboard.append({"name": "💿 ПО"})

    if len(keyboard) > 0:
        msg.inline_buttons(keyboard)
    if mobile != 20:
        msg.inline_buttons({"name": "📱 Телефон"})
    msg.inline_buttons({"name": "⭐ Усиления"})

    await msg(text)

@handler.message(name = 'компьютер', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    computer = user.hacker.get(user=user).computer
    text = f'{user()} '
    if computer != 20:
        if user.balance - (400 * computer) >= 0:
            Hacker.objects.filter(user=user).update(computer = computer + 1)
            Hacker.objects.filter(user=user).update(income_hack = user.hacker.get(user=user).income_hack + 1)
            user.balance -= Decimal(400 * computer)
            user.save()
            text += f'вы успешно улучшили компьютер до {user.hacker.get(user=user).computer} уровня {user.emoji()}'
        else:
            text += f'у вас не достаточно денег {user.emoji_bad()}'
    else:
        text += f'ваш компьютер максимально улучшен {user.emoji_bad()}'

    await msg(text)

@handler.message(name = 'по', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    programm = user.hacker.get(user=user).programm 
    text = f'{user()} '
    if programm != 20:
        if user.balance - (350 * programm) >= 0:
            Hacker.objects.filter(user=user).update(programm = programm + 1)
            Hacker.objects.filter(user=user).update(income_hack = user.hacker.get(user=user).income_hack + 1)
            user.balance -= Decimal(350 * programm)
            user.save()
            text += f'вы успешно улучшили свое программное обеспечение до {user.hacker.get(user=user).programm} уровня {user.emoji()}'
        else:
            text += f'у вас не достаточно денег {user.emoji_bad()}'
    else:
        text += f'ваше программное обеспечение максимально улучшено {user.emoji_bad()}'

    await msg(text)

@handler.message(name = 'телефон', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    mobile = user.hacker.get(user=user).mobile
    text = f'{user()} '
    if mobile != 20:
        if user.balance - (200 * mobile) >= 0:
            Hacker.objects.filter(user=user).update(mobile = mobile + 1)
            Hacker.objects.filter(user=user).update(income_hack = user.hacker.get(user=user).income_hack + 1)
            user.balance -= Decimal(200 * mobile)
            user.save()
            text += f'вы успешно улучшили телефон до {user.hacker.get(user=user).mobile} уровня {user.emoji()}'
        else:
            text += f'у вас не достаточно денег {user.emoji_bad()}'
    else:
        text += f'ваш телефон максимально улучшен {user.emoji_bad()}'

    await msg(text)
