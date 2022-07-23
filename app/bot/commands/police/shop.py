from app.bot import handler
from decimal import Decimal
from random import randint as random
from app.models import Account, Police

@handler.message(name = 'магазин', dialog = Account.Dialog.POLICE)
async def _(msg, user):
    equipment = user.police.get(user=user).equipment 
    transport = user.police.get(user=user).transport 
    text = f'{user()} улучшения:\n'
    text += f'\n🚓 Транспорт: \n&#12288;⭐ Уровень {transport}' + (f'\n&#12288;💳 Стоимость: {user.digit_number(6000 * transport)} $\n' if transport != 30 else "\n&#12288;💡 Максимально улучшен.\n")
    text += f'\n💻 Оборудование:\n&#12288;⭐ Уровень {equipment}' + (f'\n&#12288;💳 Стоимость: {user.digit_number(3000 * equipment)} $\n' if equipment != 30 else "\n&#12288;💡 Максимально улучшено.\n")
    text += f"\n💳 Баланс: {user.digit_number(int(user.balance))} $"
    text += f'\n\n💡 Улучшая данные предметы, вы увеличиваете свою удачу и заработок {user.emoji()}'

    keyboard = []
    if transport + equipment != 60:
        if transport != 30:
            keyboard.append({"name": "🚓 Транспорт"})
        if equipment != 30:
            keyboard.append({"name": "💻 Оборудование"})

    if len(keyboard) > 0:
        msg.inline_buttons(keyboard)

    msg.inline_buttons({"name": "⭐ Усиления"})

    await msg(text)

@handler.message(name = 'транспорт', dialog = Account.Dialog.POLICE)
async def _(msg, user):
    transport = user.police.get(user=user).transport 
    text = f'{user()} '
    if transport != 30:
        if user.balance - (6000 * transport) >= 0:
            Police.objects.filter(user=user).update(transport = transport + 1)
            Police.objects.filter(user=user).update(income_arrest = user.police.get(user=user).income_arrest + 1)
            user.balance -= Decimal(6000 * transport)
            user.save()
            text += f'вы успешно улучшили транспорт до {user.police.get(user=user).transport} уровня {user.emoji()}'
        else:
            text += f'у вас не достаточно денег {user.emoji_bad()}'
    else:
        text += f'ваш транспорт максимально улучшен {user.emoji_bad()}'

    await msg(text)

@handler.message(name = 'оборудование', dialog = Account.Dialog.POLICE)
async def _(msg, user):
    equipment = user.police.get(user=user).equipment
    text = f'{user()} '
    if equipment != 30:
        if user.balance - (3000 * equipment) >= 0:
            Police.objects.filter(user=user).update(equipment = equipment + 1)
            Police.objects.filter(user=user).update(income_arrest = user.police.get(user=user).income_arrest + 1)
            user.balance -= Decimal(3000 * equipment)
            user.save()
            text += f'вы успешно улучшили свое оборудование до {user.police.get(user=user).equipment} уровня {user.emoji()}'
        else:
            text += f'у вас не достаточно денег {user.emoji_bad()}'
    else:
        text += f'ваше оборудование максимально улучшено {user.emoji_bad()}'

    await msg(text)