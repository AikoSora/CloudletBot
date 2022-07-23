from app.bot import handler
from app.models import Account
from app.bot.Message import Message

@handler.message(name = 'помощь', dialog = Account.Dialog.POLICE)
async def _(msg: Message, user: Account):
	text = f"{user()} помощь:"
	text += "\n📋 Профиль - статистика"
	text += "\n🏷 Ник - установить ник"
	text += "\n🚨 Работать"
	text += "\n👥 Команда - создай свою команду!"
	text += "\n\n⚙ Настройки - настройки аккаунта"
	text += "\n&#12288;📋 Гиперссылка"
	text += "\n&#12288;📜 Рассылка"
	text += "\n\n👑 Топ - топ полицейских"
	text += "\n&#128722; Магазин"
	await msg(text)
