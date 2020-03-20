from vk.bot.dispatcher import Dispatcher
import logging
import asyncio


class Updater:
    def __init__(self, vk, group_id, wait=25):
        self.vk = vk
        self.group_id = group_id
        self.wait = 25
        self.dispatcher = Dispatcher(vk)
        self.server = None
        self.key = None
        self.ts = None

    async def get_long_poll_server(self):
        long_poll_server = await self.vk.get('groups.getLongPollServer', group_id=self.group_id)
        logging.info(str(long_poll_server))
        self.server = long_poll_server['server']
        self.key = long_poll_server['key']
        self.ts = long_poll_server['ts']

    def update_ts(self, ts):
        self.ts = ts

    async def process_updates(self, updates):
        updates = updates['updates']
        threads = []
        for update in updates:
            threads.append(self.dispatcher.process_update(update))
        await asyncio.gather(*threads)

    async def start_polling(self):
        await self.get_long_poll_server()
        while True:
            kwargs = dict(
                custom_url=self.server,
                act='a_check',
                key=self.key,
                ts=self.ts,
                wait=self.wait
            )
            updates = await self.vk.get(**kwargs)
            logging.info(updates)
            await self.process_updates(updates)
            self.update_ts(updates['ts'])
