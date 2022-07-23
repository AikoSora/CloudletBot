from app.bot.assets import Command
from app.bot.assets import PayloadCommand
from app.bot.assets import CallbackCommand

commands = []
payload_commands = []
callback_commands = []

def message(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                commands.append(Command(name=cmd, handler=handler,
                    dialog=kwargs['dialog'] if 'dialog' in kwargs else 'all',
                    admin=(kwargs['admin'] if 'admin' in kwargs else False),
                    with_args=(kwargs['with_args'] if 'with_args' in kwargs else False)))
        else:
            return False
    return with_args

def payload(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                payload_commands.append(PayloadCommand(name=cmd, handler=handler,
                    dialog=kwargs['dialog'] if 'dialog' in kwargs else 'all'))
        else:
            return False
    return with_args

def callback(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                callback_commands.append(CallbackCommand(name=cmd, handler=handler,
                    dialog=kwargs['dialog'] if 'dialog' in kwargs else 'all'))
        else:
            return False
    return with_args