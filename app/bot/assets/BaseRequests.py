import traceback, sys, asyncio

class Command:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler', 'admin'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name']
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']
        self.admin = kwargs['admin']
        self.with_args = kwargs['with_args']

    async def handle(self, msg, user):
        async def command_handler():
            try:
                await self.__handler(msg, user)
            except Exception:
                ex_type, ex, tb = sys.exc_info()
                print(ex, traceback.format_tb(tb))
                await msg('❌ Произошла ошибка, попробуйте чуть позже', reply_to=msg.id)
                await msg(sticker_id=8471)

        asyncio.ensure_future(command_handler())

class PayloadCommand:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name']
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']

    async def handle(self, msg, user):
        async def command_handler():
            try:
                await self.__handler(msg, user)
            except Exception:
                ex_type, ex, tb = sys.exc_info()
                print(ex, traceback.format_tb(tb))
                await msg('❌ Произошла ошибка, попробуйте чуть позже', reply_to=msg.id)
                await msg(sticker_id=8471)

        asyncio.ensure_future(command_handler())

class CallbackCommand:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name']
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']

    async def handle(self, msg, user):
        async def command_handler():
            try:
                await self.__handler(msg, user)
            except Exception:
                ex_type, ex, tb = sys.exc_info()
                print(ex, traceback.format_tb(tb))
                await msg('❌ Произошла ошибка, попробуйте чуть позже', reply_to=msg.id)
                await msg(sticker_id=8471)

        asyncio.ensure_future(command_handler())