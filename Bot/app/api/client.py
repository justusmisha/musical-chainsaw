import asyncio
import aiohttp

from Bot.app.data.config import ERROR_MESSAGE
from Bot.app.bot_loader import bot
from logger import logger


class StatusCodeHandler:
    def __init__(self, status_code: int, user_id: str):
        self.status_code = status_code
        self.user_id = user_id

    async def send_message_statuscode_based(self):
        try:
            if self.user_id is not None:
                if 500 <= self.status_code < 600:
                    await bot.send_message(text='❌ Произошла системная ошибка\n\n'
                                                f'{ERROR_MESSAGE}', chat_id=self.user_id)
                    return
            return
        except Exception as e:
            logger.info(f'Error handling message: {e}')


class APIClient:
    def __init__(self, base_url, timeout=10):
        self.current_base_url = base_url
        self.timeout = timeout

    def _build_url(self, url_template, **url_params):
        return self.current_base_url + url_template.format(**url_params)

    async def _request(self, method, url_template, **request_kwargs):
        url_params = {k: v for k, v in request_kwargs.items() if k not in ['json', 'data', 'headers', 'params']}
        url = self._build_url(url_template, **url_params)

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.request(method, url, **{k: v for k, v in request_kwargs.items() if
                                                           k in ['json', 'data', 'headers', 'params']}
                                           ) as response:

                    if 400 <= response.status < 500:
                        logger.error(f"Client error {response.status} for {url}")
                        return False
                    elif 500 <= response.status < 600:
                        logger.error(f"Server error {response.status} for {url}")
                        user_id = request_kwargs.get('user_id', '')
                        if user_id != '':
                            s = StatusCodeHandler(response.status, request_kwargs['user_id'])
                            await s.send_message_statuscode_based()
                        return None
                    response.raise_for_status()
                    return await response.json()
        except asyncio.TimeoutError:
            logger.error(f"Timeout error for {url}")
        except aiohttp.ClientResponseError as e:
            logger.error(f"Error {e.status} for {url}: {e.message}")
            user_id = request_kwargs.get('user_id', '')
            if user_id != '':
                s = StatusCodeHandler(response.status, request_kwargs['user_id'])
                await s.send_message_statuscode_based()
            if 400 <= e.status < 500:
                return False
            elif 500 <= e.status < 600:
                return None
        except aiohttp.ClientError as e:
            logger.error(f"Request error for {url}: {e}")
        logger.error(f"Failed to complete request after trying all base URLs")
        return None

    async def get(self, url_template, **kwargs):
        return await self._request('GET', url_template, **kwargs)

    async def post(self, url_template, data=None, json=None, **kwargs):
        return await self._request('POST', url_template, data=data, json=json, **kwargs)

    async def put(self, url_template, data=None, json=None, **kwargs):
        return await self._request('PUT', url_template, data=data, json=json, **kwargs)

    async def delete(self, url_template, **kwargs):
        return await self._request('DELETE', url_template, **kwargs)