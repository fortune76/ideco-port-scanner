import random

from aiohttp.http_exceptions import HttpBadRequest

from logs import logger
from aiohttp import web
from scanner import get_data


async def handle(request):
    """
    Обработчик требуемого урла
    """
    logger.info(f'Incoming new request')
    data_to_return = get_data(request)
    if 'Error' in data_to_return:
        logger.error(f'Bad request. request: {request}.')
        return web.json_response(data_to_return, status=401)
    return web.json_response(data_to_return)


app = web.Application()
app.add_routes([web.get('/scan/{ip}/{port_start}/{port_end}/', handle)])
app.add_routes([web.get('/scan/{ip}/{port_start}/{port_end}', handle)])


if __name__ == '__main__':
    logger.info('Ideco port checker runned succeful. Waiting for requests.')
    web.run_app(app)
