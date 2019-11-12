from aiohttp import web
from services.SNServices import addFileToNode, readFile, getFileList

# receive file and send it to relative node
async def addFileHandler(request):
    filename = request.match_info['filename']
    addFileToNode(filename)
    return web.Response()

#read the target file and return it
async def readFileHandler(request):
    filenames = request.match_info['filename']
    content = readFile(filenames)
    return web.json_response({filenames : content})
    # return web.Response(text = content)

#return the list of files stored in current node
async def getFileListHandler(request):
    FileList = getFileList()
    return web.Response(text = (", ".join(str(f) for f in FileList)))


routes = [web.post('/file/{filename}', addFileHandler),
          web.get('/file/{filename}', readFileHandler),
          web.get('/filelist', getFileListHandler)]