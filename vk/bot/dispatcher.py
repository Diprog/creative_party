class Dispatcher:
    def __init__(self, vk):
        self.vk = vk
        self.handlers = []

    def add_handler(self, handler):
        handler.vk = self.vk
        self.handlers.append(handler)

    async def process_update(self, update):
        update_type = update['type']
        for handler in self.handlers:
            await handler.handle(update)