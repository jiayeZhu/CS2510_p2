from aiohttp import web
from services import getStorageNodeStatus, refreshStorgateNodeStatus


async def heartBeatHandler(request):
    storageNodeId = int(request.match_info['id'])
    refreshStorgateNodeStatus(storageNodeId)
    return web.Response()


async def getSNStatusHandler(request):
    status = getStorageNodeStatus()
    return web.json_response({'status': status})


routes = [web.get('/sn_status', getSNStatusHandler),
          web.put('/hb/{id}', heartBeatHandler)]
