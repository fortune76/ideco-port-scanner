from logs import logger
from aiohttp import web
from scanner import get_data


async def handle(request):
    """
    Обработчик требуемого урла
    """
    logger.info(f'Incoming request {request}')
    data_to_return = web.json_response(get_data(request))
    return data_to_return


app = web.Application()
app.add_routes([web.get('/scan/{ip}/{port_start}/{port_end}/', handle)])
app.add_routes([web.get('/scan/{ip}/{port_start}/{port_end}', handle)])


if __name__ == '__main__':
    logger.info('Ideco port checker runned succeful. Waiting for requests.')
    web.run_app(app)
