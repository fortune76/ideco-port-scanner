from aiohttp.test_utils import AioHTTPTestCase

import main
from main import handle


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        async def test_handle(request):
            await handle(request)

        app = main.app
        return app

    async def test_solo_state(self):
        """
        Тест одиночного запроса при работающем сервере
        """
        async with self.client.request("GET", "/scan/0.0.0.0/8080/8080/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        self.assertIn('{"8080": "open"}', text)

    async def test_multiple_state(self):
        """
        Тест множественного запроса при работающем сервере
        """
        async with self.client.request("GET", "/scan/0.0.0.0/8079/8080/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        try:
            self.assertIn('{"8079": "close", "8080": "open"}', text)
        except:
            self.assertIn('{"8080": "open", "8079": "close"}', text)

    async def test_real_ip(self):
        """
        Тест реального ip (vk.com)
        """

        async with self.client.request("GET", "/scan/87.240.190.78/442/443/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        try:
            self.assertIn('{"442": "close", "443": "open"}', text)
        except:
            self.assertIn('{"443": "open", "442": "close"}', text)

    async def test_404(self):
        """
        Тест 404 при некорректном запросе
        """
        async with self.client.request("GET", "/scan/0.0.0.0/x/x/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        self.assertIn('{"Error": "Incorrect Values"}', text)
