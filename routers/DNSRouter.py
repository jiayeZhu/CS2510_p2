from aiohttp import web
from services import getOneDS


async def allRootHandler(request):
    path = 'http://{}/{}'.format(getOneDS(), request.match_info['path'])
    raise web.HTTPTemporaryRedirect(path)


async def allL2Handler(request):
    path = 'http://{}/{}/{}'.format(getOneDS(), request.match_info['l1path'], request.match_info['l2path'])
    raise web.HTTPTemporaryRedirect(path)

routes = [web.route('*', '/{path}', allRootHandler),
          web.route('*', '/{l1path}/{l2path}', allL2Handler)]