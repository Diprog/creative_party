class BaseHandler:
    def __init__(self):
        self.vk = None


class CommandHandler(BaseHandler):
    def __init__(self, text, func):
        super().__init__()
        self.text = text.lower()
        self.func = func

    async def handle(self, update):
        update_type = update['type']
        if update_type == 'message_new':
            message = update['object']['message']
            if self.text in message['text'].lower():
                await self.func(self.vk, update)


class WallHandler(BaseHandler):
    def __init__(self, func):
        super().__init__()
        self.func = func

    async def handle(self, update):
        update_type = update['type']
        if update_type == 'wall_post_new':
            await self.func(self.vk, update)


class CommentHandler(BaseHandler):
    pass
