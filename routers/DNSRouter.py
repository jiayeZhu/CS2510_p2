from aiohttp import web
from services import getOneDS

routes = web.RouteTableDef()


@routes.get('/')
async def root(request):
    return web.json_response({'suc': True, 'addr': getOneDS()})
