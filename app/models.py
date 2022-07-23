import re, random
from django.db import models
from time import strftime, time, localtime

class Account(models.Model):

	class TempBot:
		api = None

	class Dialog:
		START = 'start'
		DEFAULT = 'default'
		POLICE = 'police'
		HACKER = 'hacker'
		CREATE_BN = "create_bn"
		CREATE_PC = "create_pc"

	username = models.TextField(default = None, null = True, blank = True)
	user_id = models.IntegerField(default = 0)
	dialog = models.TextField(default = Dialog.START)
	balance = models.DecimalField(default = 100, max_digits = 32, decimal_places = 0)
	temp = models.TextField(default = '')
	reg_date = models.TextField(default=f'{strftime("%Y.%m.%d %H:%M", localtime(time() + 10800))}')
	hyperlink = models.IntegerField(default = 0)
	mention = models.IntegerField(default = 0)
	message_time = models.IntegerField(default = 0)
	botnet_id = models.IntegerField(default=0)
	report_time = models.IntegerField(default=0)
	donate_points = models.IntegerField(default=0)
	answer_mention = models.IntegerField(default=0)
	buffs_one_time = models.IntegerField(default=0)
	buffs_two_time = models.IntegerField(default=0)
	buffs_three_time = models.IntegerField(default=0)
	old_activation_promo_id = models.BigIntegerField(default=0)
	holiday_temp = models.BigIntegerField(default=0)
	holiday_time = models.IntegerField(default=0)

	def digit_number(self, count: int) -> str:
		return '{0:,}'.format(count).replace(',', '.')

	def emoji(self):
		emoji = ['&#128527;', '&#128522;', '&#128579;', '&#128559;']
		return random.choice(emoji)

	def emoji_bad(self):
		emoji_bad = ['😐', '😟', '😕', '😔']
		return random.choice(emoji_bad)

	def decline(seld, number, titles):
		cases = [2, 0, 1, 1, 1, 2]
		return titles[2 if (number % 100 > 4) and (number % 100 < 20) else cases[number % 10 if number % 10 < 5 else 5]]

	def __call__(self, comma = False) -> str:
		return f"[id{self.user_id}|{self.username}]{',' if not comma else ''}" if self.hyperlink else f"{self.username}{',' if not comma else ''}"

	def __str__(self):
		return '%s : %s.' % (self.username, self.id)

class Hacker(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='hacker')
	cryptocurrency = models.TextField(default="ETH")
	arrest_time = models.IntegerField(default=0)
	hack_time = models.IntegerField(default=0)
	hacks_count = models.IntegerField(default=0)
	hacks_rating = models.IntegerField(default=0)
	income_hack = models.IntegerField(default=1)
	programm = models.IntegerField(default=1)
	computer = models.IntegerField(default=1)
	mobile = models.IntegerField(default=1)
	farm_level = models.IntegerField(default=1)
	farm_time = models.IntegerField(default=0)
	answer_call = models.IntegerField(default=0)
	answer_id = models.IntegerField(default=0)
	escape_money = models.IntegerField(default=0)

class BotNet(models.Model):
	botnet_name = models.TextField(default="")
	users_count = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.id}) {self.botnet_name}"

class PoliceCommands(models.Model):
	command_name = models.TextField(default="")
	users = models.TextField(default="")
	password = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.id}) {self.command_name}"

class Police(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='police')
	income_arrest = models.IntegerField(default=1)
	arrest_count = models.IntegerField(default=0)
	arrest_rating = models.IntegerField(default=0)
	equipment = models.IntegerField(default=1)
	transport = models.IntegerField(default=1)
	work_time = models.IntegerField(default=0)

class Other(models.Model):
	hacks = models.DecimalField(default=0, max_digits=32, decimal_places=0)
	arrest = models.DecimalField(default=0, max_digits=32, decimal_places=0)
	bitcoins = models.IntegerField(default=0)
	etherium = models.IntegerField(default=0)
	count_message = models.BigIntegerField(default=0)
	block = models.TextField(default="False")
	holiday = models.BooleanField(default=False)

class Hacks(models.Model):
	text = models.TextField(default="")
	mention = models.TextField(default="")

class WorkForPolice(models.Model):
	name = models.TextField(default='')
	text = models.TextField(default="")

	def __str__(self):
		return f"{self.name}"

class PoliceSystemCall(models.Model):
	answer_call_id = models.IntegerField(default=0)

	def __str__(self):
		return "Вспомогательное поле для системы вызовов"

class UnitPayPayments(models.Model):
	vkid = models.IntegerField(default=0)
	payment_id = models.IntegerField(default=0) 
	status = models.TextField(default="")
	upay_time = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.vkid} / {self.upay_time} / {self.status}"

class Promo(models.Model):
	name = models.TextField(default="бабло")
	max_users = models.IntegerField(default=5)
	activated = models.IntegerField(default=0)
	price = models.IntegerField(default=100)

	def __str__(self):
		return f"{self.id}"