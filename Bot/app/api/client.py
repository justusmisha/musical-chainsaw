import asyncio
import aiohttp
from aiogram import types

from app_logger import logger


class StatusCodeHandler:
    def __init__(self, status_code: int, call: types.CallbackQuery):
        self.status_code = status_code
        self.call = call

    async def send_message_statuscode_based(self):
        try:
            if self.call is not None:
                if 500 <= self.status_code < 600:
                    await self.call.message.answer(text='❌ Произошла системная ошибка')
                    return
                elif self.status_code == 400:
                    await self.call.message.answer(text='❌ Произошла ошибка в связи с неверными данными.\n'
                                                        'Убедитесь, что данные введены верно.')
                    return
                elif self.status_code == 403:
                    await self.call.message.answer(text='❌ У вас нет прав доступа к этому ресурсу.\n'
                                                        'Проверьте свои права доступа.')
                    return
                elif self.status_code == 404:
                    await self.call.message.answer(text='❌ Ресурс не найден. Убедитесь, что все данные введены правильно.')
                    return
                elif self.status_code == 405:
                    await self.call.message.answer(text='❌ Метод не поддерживается на сервере.')
                    return
                elif self.status_code == 408:
                    await self.call.message.answer(text='❌ Истекло время ожидания запроса.\n'
                                                        'Попробуйте повторить запрос позднее.')
                    return
                elif self.status_code == 429:
                    await self.call.message.answer(
                        text='❌ Превышен лимит запросов. Попробуйте повторить запрос позже.')
                    return
                elif 400 <= self.status_code < 600:
                    await self.call.message.answer(text=f'❌ Произошла ошибка с кодом {self.status_code}.')
                    return
                return
            return
        except Exception as e:
            logger.info(f'Error handling message: {e}')


class APIClient:
    def __init__(self, base_urls, timeout=10):
        self.base_urls = base_urls
        self.current_base_url = base_urls[0]
        self.timeout = timeout

    def _build_url(self, url_template, **url_params):
        return self.current_base_url + url_template.format(**url_params)

    async def _request(self, method, url_template, call: types.CallbackQuery = None, **request_kwargs):
        url_params = {k: v for k, v in request_kwargs.items() if k not in ['json', 'data', 'headers', 'params']}
        url = self._build_url(url_template, **url_params)

        for base_url in self.base_urls:
            self.current_base_url = base_url
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                    async with session.request(method, url, **{k: v for k, v in request_kwargs.items() if
                                                               k in ['json', 'data', 'headers', 'params']}) as response:
                        StatusCodeHandler(response.status, call)
                        if 400 <= response.status < 500:
                            logger.error(f"Client error {response.status} for {url}")
                            return False
                        elif 500 <= response.status < 600:
                            logger.error(f"Server error {response.status} for {url}")
                            return None
                        response.raise_for_status()
                        return await response.json()
            except asyncio.TimeoutError:
                logger.error(f"Timeout error for {url}")
            except aiohttp.ClientResponseError as e:
                logger.error(f"Error {e.status} for {url}: {e.message}")
                StatusCodeHandler(response.status, call)
                if 400 <= e.status < 500:
                    return False
                elif 500 <= e.status < 600:
                    return None
            except aiohttp.ClientError as e:
                logger.error(f"Request error for {url}: {e}")
        logger.error(f"Failed to complete request after trying all base URLs")
        return None

    async def get(self, url_template, call: types.CallbackQuery = None, **kwargs):
        return await self._request('GET', url_template, call, **kwargs)

    async def post(self, url_template, data=None, json=None, call: types.CallbackQuery = None, **kwargs):
        return await self._request('POST', url_template, call, data=data, json=json, **kwargs)

    async def put(self, url_template, data=None, json=None, **kwargs):
        return await self._request('PUT', url_template, data=data, json=json, **kwargs)

    async def delete(self, url_template, **kwargs):
        return await self._request('DELETE', url_template, **kwargs)
