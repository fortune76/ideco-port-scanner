from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web

import main
from main import handle


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        async def test_handle(request):
            await handle(request)

        app = main.app
        return app

    async def test_solo_state(self):
        async with self.client.request("GET", "/scan/0.0.0.0/8080/8080/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        self.assertIn('{"8080": "close"}', text)

    async def test_multiple_state(self):
        async with self.client.request("GET", "/scan/0.0.0.0/8079/8080/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        try:
            self.assertIn('{"8079": "close", "8080": "close"}', text)
        except:
            self.assertIn('{"8078": "close", "8079": "close"}', text)

    async def test_404(self):
        async with self.client.request("GET", "/scan/0.0.0.0/x/x/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        self.assertIn('{"Error": "404 error. Use correct URL."}', text)
