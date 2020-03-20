text = 'начать'


async def command(vk, update):
    message = update['object']['message']
    await vk.reply_text('ПРИВЕТ', message)
