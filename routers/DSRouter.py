from aiohttp import web
from services import getStorageNodeStatus, refreshStorgateNodeStatus, setState


async def heartBeatHandler(request):
    storageNodeId = int(request.match_info['id'])
    refreshStorgateNodeStatus(storageNodeId)
    return web.Response()


async def getSNStatusHandler(request):
    status = getStorageNodeStatus()
    return web.json_response({'status': status})


async def syncHandler(request):
    state = await request.json()
    setState(state)
    return web.Response()

routes = [web.get('/sn_status', getSNStatusHandler),
          web.put('/hb/{id}', heartBeatHandler),
          web.put('/sync', syncHandler)]
