from json import dumps
from app.bot.LongPoll import api
from random import randint as random

class Message:

	event = None
	path_args = []
	callback = False
	text = None
	id = None

	def __init__(self, event, callback=False):
		self.event = event
		self.keyboard = {"inline": False, "one_time": False, "buttons": []}
		self.set_keyboard_default = False
		if callback:
			self.callback = True
			self.message_id = event['object']['conversation_message_id']
			self.message_event = self.event['object']['event_id']
		else:
			self.text = event['object']['message']['text']
			self.id = event['object']['message']['id']

	def buttons(self, *args):
		if self.set_keyboard_default:
			self.set_keyboard_default = False
			self.keyboard["buttons"] = []
		if self.keyboard["inline"]:
			self.keyboard["inline"] = False
			self.keyboard["buttons"] = []
		self.keyboard["buttons"].append([])
		self.check_buttons(args)

	def inline_buttons(self, *args):
		if self.set_keyboard_default:
			self.set_keyboard_default = False
			self.keyboard["buttons"] = []
		if not self.keyboard["inline"]:
			self.keyboard["inline"] = True
			self.keyboard["buttons"] = []
		self.keyboard["buttons"].append([])
		self.check_buttons(args)

	def check_buttons(self, args): # <- ([{}]) or ({}) or (({}))
		array = []
		for button in args: # <- [{}] or {} ({})
			if isinstance(button, list) or isinstance(button, tuple):
				for butt in button: # <- {}
					if not isinstance(butt, dict):
						continue
					if not butt.keys() & {'name'}:
						continue
					array.append(butt)
			else:
				if not isinstance(button, dict):
					continue
				if not button.keys() & {'name'}:
					continue
				array.append(button)
		if len(array) != 0:
			self.add_buttons(array)
		
	def add_buttons(self, args): # <- []
		for button in args:
			if not button.keys() & {'payload'} and not button.keys() & {'command'}:
				self.keyboard["buttons"][len(self.keyboard["buttons"])-1].append({"action": {"type": "text",
																						  	 "label": button['name']},
																			  	  "color": "secondary" if not button.keys() & {'color'} else button['color']})
			elif not button.keys() & {'command'} and button.keys() & {'payload'}:
				self.keyboard["buttons"][len(self.keyboard["buttons"])-1].append({"action": {"type": "text",
																							 "payload": {"button": button['payload']},
																						 	 "label": button['name']},
																			  	  "color": "secondary" if not button.keys() & {'color'} else button['color']})
			elif button.keys() & {'command'}:
				self.keyboard["buttons"][len(self.keyboard["buttons"])-1].append({"action": {"type": "callback",
																							 "payload": {"button": button['command']},
																						 	 "label": button['name']},
																			  	  "color": "secondary" if not button.keys() & {'color'} else button['color']})
	
	def keyboard_default(self):
		self.buttons([{"name": "Бонус", "color": "positive"}, {"name": "Профиль", "color": "primary"}])
		self.buttons({"name": "Помощь", "color": "positive"})
		self.set_keyboard_default = True

	async def __call__(self, text=None, attachment=None, sticker_id=None, user_id=None, user_ids=None, reply_to=None, forward_messages=None):
		if text == None and attachment == None and sticker_id == None:
			raise Exception("The text should not be empty!")
		if self.callback:
			peer_id = self.event['object']['peer_id']
		else:
			peer_id = self.event['object']['message']['peer_id'] 

		if not user_ids:
			request = {"peer_id": peer_id if user_id == None else user_id,
				   "intent": "default",
				   "message": text if text else "",
				   "reply_to": reply_to if reply_to else "",
				   "sticker_id": sticker_id if sticker_id != None else 0,
				   "attachment": attachment if attachment != None else '',
				   "random_id": random(0, 100000000)}
		else:
			request = {"peer_ids": user_ids,
				   "intent": "default",
				   "message": text if text != None else "",
				   "reply_to": reply_to if reply_to else "",
				   "sticker_id": sticker_id if sticker_id != None else 0,
				   "attachment": attachment if attachment != None else '',
				   "random_id": random(0, 100000000)}
		if forward_messages and not reply_to:
			request.update({"forward_messages": forward_messages})
		if len(self.keyboard['buttons']) != 0:
			if len(self.keyboard["buttons"][0]) != 0:
				request.update({'keyboard': dumps(self.keyboard)})
				self.keyboard['buttons'] = []

		return await api("messages.send", request)

	@staticmethod
	async def send(text=None, attachment=None, sticker_id=None, user_id=None, user_ids=None):
		if text == None and attachment == None and sticker_id == None:
			raise Exception("The text should not be empty!")

		if not user_ids:
			request = {"peer_id": user_id,
				   "intent": "default",
				   "message": text if text != None else "",
				   "sticker_id": sticker_id if sticker_id != None else 0,
				   "attachment": attachment if attachment != None else '',
				   "random_id": random(0, 100000000)}
		else:
			request = {"peer_ids": user_ids,
				   "intent": "default",
				   "message": text if text != None else "",
				   "sticker_id": sticker_id if sticker_id != None else 0,
				   "attachment": attachment if attachment != None else '',
				   "random_id": random(0, 100000000)}


		return await api("messages.send", request)

	async def edit(self, text=None, attachment=None):
		if text == None and attachment == None:
			raise Exception("The text should not be empty!")
		if self.callback == False:
			raise Exception("this method in msg is only available for callback buttons")

		request = {"peer_id": self.event['object']['peer_id'],
				   "message": text if text != None else "",
				   "attachment": attachment if attachment != None else '',
				   "conversation_message_id": self.message_id}

		if len(self.keyboard['buttons']) != 0:
			request.update({'keyboard': dumps(self.keyboard)})
			self.keyboard['buttons'] = []

		return await api("messages.edit", request)

	async def snackbar(self, text):
		if self.callback == False:
			raise Exception("this method in msg is only available for callback buttons")

		request = {"event_id": self.message_event,
				  "user_id": self.event['object']['user_id'],
				  "peer_id": self.event['object']['peer_id'],
				  "event_data": dumps({"type": "show_snackbar", "text": str(text)[:90]})}

		return await api("messages.sendMessageEventAnswer", request)