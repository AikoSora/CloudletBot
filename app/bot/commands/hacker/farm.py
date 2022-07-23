import time
from decimal import Decimal
from app.bot import handler
from random import randint as random
from app.models import Account, Hacker
from app.bot.commands.func import btc, eth

etherium_currency = 0.00200016
bitcoin_currency = 0.00130000

@handler.message(name = 'ферма', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    hack_account = Hacker.objects.get(user=user)
    currency = etherium_currency if hack_account.cryptocurrency == "ETH" else bitcoin_currency
    if hack_account.farm_time != 0:
        money_time = (int(time.time()) - int(hack_account.farm_time)) / 3600
    else:
        money_time = 0
        hack_account.farm_time = time.time()
        hack_account.save()
    money = (currency * hack_account.farm_level) * int(money_time)
    text = f"{user()} ваша ферма:"
    text += '\n💰 Доход: {0:.8f}/ч {1}'.format(currency * hack_account.farm_level, hack_account.cryptocurrency)
    text += '\n💳 Добыто: {0:.8f} $'.format(eth(money) if hack_account.cryptocurrency == "ETH" else btc(money))
    text += f'\n⭐ Уровень: {hack_account.farm_level}'
    text += f'\n💰 Стоимость улучшения: {100 * hack_account.farm_level} $' if hack_account.farm_level != 20 else ''
    text += f'\n\nУлучшайте свою ферму, увеличивайте заработок {user.emoji()}' if hack_account.farm_level != 20 else ''

    keyboard = []

    if hack_account.farm_level != 20:
        keyboard.append({'name': "⭐ Улучшить"})
    if hack_account.cryptocurrency != 'BTC':
        keyboard.append({'name': "💳 BTC"})

    if len(keyboard) > 0:
        msg.inline_buttons(keyboard)
    msg.inline_buttons({"name": "💰 Снять"})

    await msg(text, attachment = "photo-198059264_457239505")

@handler.message(name = 'улучшить', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    text = f'{user()} '
    level = user.hacker.get(user=user).farm_level
    if level != 20:
        if user.balance - (100 * level) >= 0:
            money_time = (int(time.time()) - int(Hacker.objects.get(user=user).farm_time)) / 3600
            money = (etherium_currency * Hacker.objects.get(user=user).farm_level) * int(money_time)
            user.balance += Decimal(eth(money))
            Hacker.objects.filter(user=user).update(farm_level = level + 1, farm_time=time.time())
            user.balance -= Decimal(100 * level)
            user.save()
            text += f'вы успешно улучшили свою ферму до {user.hacker.get(user=user).farm_level} уровня\nОставшиеся деньги были переведены на ваш счет {user.emoji()}'
        else:
            text += f'у вас не достаточно денег {user.emoji_bad()}'
    else:
        text += f'ваша ферма максимально улучшена {user.emoji_bad()}'

    await msg(text)

@handler.message(name = 'btc', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    text = f'{user()} '
    if user.hacker.get(user=user).cryptocurrency != 'BTC':
        if user.hacker.get(user=user).hacks_rating >= 75:
            money_time = (int(time.time()) - int(Hacker.objects.get(user=user).farm_time)) / 3600
            money = (etherium_currency * Hacker.objects.get(user=user).farm_level) * int(money_time)
            Hacker.objects.filter(user=user).update(cryptocurrency = 'BTC', farm_level = 1, farm_time=time.time())
            user.balance += Decimal(eth(money))
            user.save()
            text += f'вы стали добывать биткоины, оставшийся деньги были переведены на ваш счет {user.emoji()}'

            msg.inline_buttons({"name": "💽 Ферма"})
            await msg(text)
    
        else:
            text += f'добыча биткоинов доступна с 75 взломов! {user.emoji_bad()}'
            await msg(text)
    else:
        await msg(f"{text}вы уже добываете биткоины {user.emoji_bad()}")

@handler.message(name = 'снять', dialog = Account.Dialog.HACKER)
async def _(msg, user):
    text = f'{user()} '
    currency = etherium_currency if Hacker.objects.get(user=user).cryptocurrency == "ETH" else bitcoin_currency
    hacker_account = Hacker.objects.get(user=user)
    if hacker_account.farm_time != 0:
        money_time = (int(time.time()) - int(hacker_account.farm_time)) / 3600
    else:
        money_time = 0
        hacker_account.farm_time = time.time()
        hacker_account.save()

    money = (currency * hacker_account.farm_level) * int(money_time)

    if money != 0:
        user.balance += Decimal(eth(money) if hacker_account.cryptocurrency == "ETH" else btc(money))
        Hacker.objects.filter(user=user).update(farm_time = time.time())
        user.save()
        text += 'вы успешно сняли {0:.8f} $ {1}'.format(float(eth(money) if hacker_account.cryptocurrency == "ETH" else btc(money)), user.emoji())
    else:
        text += f'ферма еще не добыла криптовалюту {user.emoji_bad()}'
    await msg(text)