import aiohttp
import logging
from vk.errors import *
import time


class VKAPI:
    VERSION = '5.103'
    ENDPOINT = 'https://api.vk.com/method/'

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    def __init__(self, tokens=None, token_fail_hook=None, max_retries=5):
        self.session = None
        self.tokens = tokens
        self.token_fail_hook = token_fail_hook
        self.token_pos = 0
        self.max_retries = max_retries

    def load_tokens(self, tokens):
        self.tokens = tokens

    def switch_token(self):
        if self.token_pos + 1 >= len(self.tokens):
            self.token_pos = 0
        else:
            self.token_pos += 1

    def token_fail(self, error_code):
        failed_token = self.tokens[self.token_pos]
        del self.tokens[self.token_pos]
        if self.token_fail_hook:
            self.token_fail_hook(failed_token, error_code)

    def set_default_request_params(self, params):
        # Если токены не были предоставлены, то ждём, пока это произойдёт.
        if not self.tokens:
            logging.info('Ожидание токенов...')
            while not self.tokens:
                pass
        try:
            params['access_token'] = self.tokens[self.token_pos]
        except IndexError:
            self.token_pos = 0
        params['v'] = VKAPI.VERSION

    async def request(self, request_method, vk_method, custom_url=None, retry=0, **params):
        self.set_default_request_params(params)

        args = dict(method=request_method,
                    url=custom_url if custom_url else VKAPI.ENDPOINT + vk_method,
                    params=params if request_method == 'get' else None,
                    data=params if request_method == 'post' else None)

        async with self.session.request(**args) as r:
            if r.status == 200:
                json = await r.json()
                error = json.get('error')
                response = json.get('response')
                ts = json.get('ts')
                if error:
                    error_code = error['error_code']
                    if error_code in (6, 10):
                        if not retry:
                            logging.info('retrying ' + str(error))
                        self.switch_token()
                        return await self.request(request_method, vk_method, retry=retry + 1, **params)
                    elif error_code in (5, 29):
                        self.token_fail(error_code)
                        return await self.request(request_method, vk_method, retry=retry + 1, **params)
                    else:
                        raise VKError(error)
                elif response:
                    return response
                elif ts:
                    return json
            else:
                print(r.status)

    async def get(self, method=None, **params):
        return await self.request('get', method, **params)

    async def post(self, method=None, **params):
        return await self.request('post', method, **params)

    async def execute(self, code):
        return await self.post('execute', code=code)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def reply_text(self, text, message):
        return await self.get('messages.send',
                              user_id=message['from_id'],
                              random_id=int(time.time() * 10000000),
                              message=text)

