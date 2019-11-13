from aiohttp import web
from services import getOneDS,regOneDS,getDSList, refreshDirectoryServerStatus


async def allRootHandler(request):
    path = 'http://{}/{}'.format(getOneDS(), request.match_info['path'])
    raise web.HTTPTemporaryRedirect(path)


async def allL2Handler(request):
    path = 'http://{}/{}/{}'.format(getOneDS(), request.match_info['l1path'], request.match_info['l2path'])
    raise web.HTTPTemporaryRedirect(path)


async def dsRegHandler(request):
    addr = request.match_info['addr']
    regOneDS(addr)
    return web.Response()


async def getDsListHandler(request):
    cmd = request.match_info['cmd']
    return web.json_response({'ds_list': getDSList(cmd != 'all')})


async def dsHeartBeatHandler(request):
    id = request.match_info['id']
    refreshDirectoryServerStatus(int(id))
    return web.Response()


routes = [web.route('*', '/{path}', allRootHandler),
          web.route('*', '/{l1path}/{l2path}', allL2Handler),
          web.post('/ds/list/{addr}', dsRegHandler),
          web.get('/ds/list/{cmd}', getDsListHandler),
          web.put('/ds/hb/{id}',dsHeartBeatHandler)]