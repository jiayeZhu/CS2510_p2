from aiohttp import web
from services.SNServices import addFileToNode, readFile, getFileList

# receive file and send it to relative node
async def addFileHandler(request):
    filename = request.match_info['filename']
    content = await request.read()
    await addFileToNode(filename, content)
    return web.Response()

#read the target file and return it
async def readFileHandler(request):
    filename = request.match_info['filename']
    response = await readFile(filename)
    if response:
        if isinstance(response,str):
            # print('http://{}/file/{}'.format(response,filename))
            raise web.HTTPTemporaryRedirect('http://{}/file/{}'.format(response,filename))
        else:
            return web.Response(body=response)
    else:
        raise web.HTTPNotFound

#return the list of files stored in current node
async def getFileListHandler(request):
    FileList = getFileList()
    return web.json_response({'fileList':getFileList()})


routes = [web.post('/file/{filename}', addFileHandler),
          web.get('/file/{filename}', readFileHandler),
          web.get('/filelist', getFileListHandler)]