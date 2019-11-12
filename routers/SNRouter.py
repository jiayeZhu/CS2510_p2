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
    return web.json_response({'filename':filename, 'content':response})

#return the list of files stored in current node
async def getFileListHandler(request):
    FileList = getFileList()
    return web.json_response({'fileList:':getFileList()})


routes = [web.post('/file/{filename}', addFileHandler),
          web.get('/file/{filename}', readFileHandler),
          web.get('/filelist', getFileListHandler)]