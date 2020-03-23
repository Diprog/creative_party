from bot.keyboards import MainKeyboard
import strings
import constants.vk
text = 'начать'


async def command(vk, update):
    message = update['object']['message']
    is_member = await vk.get('groups.isMember', group_id=update['group_id'], user_id=message['from_id'])
    if is_member:
        await vk.reply_text(strings.get('START_MSG'), message, keyboard=MainKeyboard())
