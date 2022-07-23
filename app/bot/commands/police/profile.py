from time import time
from json import dumps
from app.bot import handler
from random import randint as random
from app.models import Account, Police, PoliceCommands, Other
from app.bot.Message import Message

keyboard_profile = (
                        {"name": "⚙ Настройки", "command": "settings", "color": "secondary"},
                        {"name": "👑 Топ", "color": "secondary"}
                    )
keyboard_settings = (
                        {"name": "📋 Гиперссылка", "command": "hyperlink", "color": "secondary"},
                        {"name": "📰 Рассылка", "command": "mention", "color": "secondary"}
                    )

async def profile(msg: Message, user: Account, callback: bool = False):
    luck = None
    name = None
    if user.botnet_id != 0:
        luck = PoliceCommands.objects.get(id=user.botnet_id)
        name = luck.command_name
        luck = len(luck.users.replace(".", " ").strip().split())
    police = Police.objects.get(user=user)
    text = f"{user()} профиль:"
    text += '\n💴 Баланс: {} $'.format(int(user.balance))
    text += f"\n💷 Баллы: {user.donate_points}"
    text += f'\n🔐 Совершено арестов: {police.arrest_rating}'
    text += f'\n👑 Рейтинг: {police.arrest_count}'
    text += f'\n☘ Удача: {(police.transport + police.equipment) + (0 if int(time()) >= user.buffs_one_time else 10)} ур. ' + (f"(+{luck} - {name})" if user.botnet_id != 0 else "")
    text += f'\n🎁 Получено: {user.holiday_temp} {user.decline(user.holiday_temp, ["подарок", "подарка", "подарков"])}'
    text += f'\n\n📅 Дата регистрации: {user.reg_date}'
    
    msg.inline_buttons(keyboard_profile)

    if callback:
        await msg.edit(text)
    else:
        await msg(text)

async def settings(msg: Message, user: Account, callback: bool = False):
    text = f'{user()} настройки:'
    text += f'\n📋 Гиперссылка: {"вкл" if user.hyperlink else "выкл"}'
    text += f'\n📰 Рассылка: {"вкл" if user.mention else "выкл"}'
    
    msg.inline_buttons(keyboard_settings)

    if callback:
        msg.inline_buttons({"name": "🔙 Назад", "command": "profile", "color": "secondary"})
        await msg.edit(text)
    else:
        await msg(text)

async def hyperlink(msg: Message, user: Account, callback: bool = False):
    if user.hyperlink:
        user.hyperlink = False
        user.save()
        text = f"{user()} гиперссылка отключена {user.emoji()}"
    elif not user.hyperlink:
        user.hyperlink = True
        user.save()
        text = f"{user()} гиперссылка включена {user.emoji()}"

    if callback:
        msg.inline_buttons({"name": "🔙 Назад", "command": "settings", "color": "secondary"})
        await msg.edit(text)
    else:
        await msg(text)

async def mention(msg: Message, user: Account, callback: bool = False):
    if user.mention:
        user.mention = False
        user.save()
        text = f"{user()} вы отписались от рассылки {user.emoji()}"
    elif not user.mention:
        user.mention = True
        user.save()
        text = f"{user()} вы подписались на рассылку {user.emoji()}"

    if callback:
        msg.inline_buttons({"name": "🔙 Назад", "command": "settings", "color": "secondary"})
        await msg.edit(text)
    else:
        await msg(text)

# PROFILE
@handler.message(name = ['профиль','проф','стата', 'статистика'], dialog = Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await profile(msg, user)

@handler.callback(name="profile", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await profile(msg, user, True)

@handler.payload(name="profile", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await profile(msg, user)

# SETTINGS
@handler.callback(name="settings", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await settings(msg, user, True)

@handler.payload(name="settings", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await settings(msg, user)

@handler.message(name = 'настройки', dialog = Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await settings(msg, user)

# HYPERLINK
@handler.message(name = 'гиперссылка', dialog = Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await hyperlink(msg, user)

@handler.callback(name="hyperlink", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await hyperlink(msg, user, True)

@handler.payload(name="hyperlink", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await hyperlink(msg, user)

# MENTION
@handler.message(name = 'рассылка', dialog = Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await mention(msg, user)

@handler.callback(name="mention", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await mention(msg, user, True)

@handler.payload(name="mention", dialog=Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
    await mention(msg, user)
