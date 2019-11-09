from aiohttp import web
from services import getStorageNodeStatus, refreshStorgateNodeStatus, setState, addFileToFileList, connect, getFileList


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


async def connectHandler(request):
    connectNodeId = await connect()
    return web.json_response({'SN' : connectNodeId})


async def getFileListHandler(request):
    FileList = getFileList()
    return web.Response(text = (", ".join(str(f) for f in FileList)))


async def addFileHandler(request):
    files = list(request.match_info['filename'])
    addFileToFileList(files)
    return web.Response()


routes = [web.get('/sn_status', getSNStatusHandler),
          web.put('/hb/{id}', heartBeatHandler),
          web.put('/sync', syncHandler),
          web.get('/connect', connectHandler),
          web.get('/filelist', getFileListHandler),
          web.post('/file/{filename}', addFileHandler)]
