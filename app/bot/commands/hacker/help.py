from app.bot import handler
from app.models import Account
from app.bot.Message import Message

@handler.message(name = 'помощь', dialog = Account.Dialog.HACKER)
async def _(msg: Message, user: Account):
	text = f"{user()} помощь:"
	text += "\n📋 Профиль - статистика"
	text += "\n🏷 Ник - установить ник"
	text += "\n👾 Взлом - совершить взлом"
	text += "\n💻 Ботнет - создай свою ботнет сеть"
	text += "\n\n⚙ Настройки - настройки аккаунта"
	text += "\n&#12288;📋 Гиперссылка"
	text += "\n&#12288;📜 Рассылка"
	text += "\n\n👑 Топ - топ хакеров"
	text += "\n&#128722; Магазин"
	text += "\n\n💽 Ферма"
	text += "\n&#12288;💰 Снять"
	text += "\n&#12288;⭐ Улучшить"
	text += "\n&#12288;💳 BTC"
	await msg(text)