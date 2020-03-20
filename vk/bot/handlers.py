class CommandHandler:
    def __init__(self, text, func):
        self.vk = None
        self.text = text.lower()
        self.func = func

    async def handle(self, update):
        update_type = update['type']
        objects = update['object']
        if update_type == 'message_new':
            message = update['object']['message']
            if self.text in message['text'].lower():
                await self.func(self.vk, update)

class WallHandler:
    pass

class CommentHandler:
    pass