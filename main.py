from logs import logger
from aiohttp import web
from scanner import port_scanner_loop, get_data


async def handle(request):
    try:
        logger.info('Incoming request')
        return web.json_response(get_data(request))
    except Exception:
        logger.error('Request error')
        return web.json_response({'Error': 'Request_error'})


app = web.Application()
app.add_routes([web.get('/scan/{ip}/{port_start}/{port_end}/', handle)])

if __name__ == '__main__':
    logger.info('Ideco port checker runned succeful')
    web.run_app(app)