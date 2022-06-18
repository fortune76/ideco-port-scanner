from logs import logger
from aiohttp import web
from scanner import get_data


async def handle(request):
    """
    Обработчик требуемого урла
    """
    try:
        logger.info('Incoming request')
        return web.json_response(get_data(request))
    except Exception:
        logger.error('Request error')
        return web.json_response({'Error': 'Request_error'})


@web.middleware
async def error_middleware(request, handler):
    """
    Отлавливание 404, если урл не корректен.
    """
    try:
        response = await handler(request)
        if response.status != 404:
            return response
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
    return web.json_response({'Error': '404 error. Use correct URL.'})


app = web.Application(middlewares=[error_middleware])
app.add_routes([web.get('/scan/{ip}/{port_start}/{port_end}/', handle)])


if __name__ == '__main__':
    logger.info('Ideco port checker runned succeful')
    web.run_app(app)