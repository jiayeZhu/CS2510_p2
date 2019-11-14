from aiohttp import web
from services import getStorageNodeStatus, refreshStorgateNodeStatus, setState, addFileToFileList, connect, getFileList, getDSState,setStorageNodeStatue


async def heartBeatHandler(request):
    storageNodeId = int(request.match_info['id'])
    await refreshStorgateNodeStatus(storageNodeId)
    return web.Response()


async def getSNStatusHandler(request):
    status = getStorageNodeStatus()
    return web.json_response({'status': status})


async def syncHandler(request):
    state = await request.json()
    if not state['hbsync']:
        setState(state)
    else:
        hbid = state['hbid']
        setStorageNodeStatue(hbid)
    return web.Response()


async def getStateHandler(request):
    return web.json_response(getDSState())


async def connectHandler(request):
    connectNodeId = await connect()
    return web.json_response({'SN' : connectNodeId})


async def getFileListHandler(request):
    return web.json_response({'fileList:':getFileList()})


async def addFileHandler(request):
    files = [(request.match_info['filename'])]
    await addFileToFileList(files)
    return web.Response()


async def getAliveSNListHandler(request):
    status = getStorageNodeStatus()
    result = [i+1 for i in range(8) if status[i] != 0]
    return web.json_response({'alive_sn_list':result})

routes = [web.get('/sn_status', getSNStatusHandler),
          web.put('/hb/{id}', heartBeatHandler),
          web.put('/sync', syncHandler),
          web.get('/sync', getStateHandler),
          web.get('/connect', connectHandler),
          web.get('/filelist', getFileListHandler),
          web.post('/file/{filename}', addFileHandler),
          web.get('/alive_snlist',getAliveSNListHandler)]
