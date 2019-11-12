import asyncio, aiohttp
import hashlib
import json

SN = {}  # nodeId : port
FILE_LIST = {}
chunk_size = 30

# can only add one file at a time, parameter files:{fileName: fileContent}
async def addFileToNode(files):
    # If the request is invoked by a directory server  TODO
    FILE_LIST.add(files.keys())
    with open(files.keys(), 'w') as f:     # path of the file TODO
        f.write(files.values())

     # If the request is invoked by a client, notify the directory server about adding the file  TODO
    async with aiohttp.ClientSession() as session:  
        async with session.post('https://127.0.0.1:18888/file/{filename}', data = files) as resp:
            await resp.text()



# can be a list of filename
async def readFile(filenames):
    response = {}
    for filename in filenames:
        # if the file is stored in the current node
        if filename in FILE_LIST:
            try:
                f = open('filename', 'r')   # path of the file in the current node TODO
                data = f.read() 
                response[filename] = data
            finally:
                if f:
                    f.close() 
        # if the file is not stored in the current node
        else:
            async with aiohttp.ClientSession() as session:
                hashKey = str(hashlib.sha1(str(filename)).hexdigest())
                nodeHashList = SN.values()
                n = len(SN)
                node = -1
                for index in range(n):
                    if(nodeHashList(index-1+n%n) < hashKey ) and (hashKey < nodeHashList(index%n)):
                        node = index
                        break
                if(node == -1) : node = 0
                count = 3
                while count > 0:
                    nodePort = SN[node]
                    async with session.get('https://127.0.0.1:{nodePort}/file/{filename}') as resp:
                        if resp.status == 200:
                            msg = json.loads(resp.json())
                            response.update(msg)
                            break
                        else:
                            print(' SN {} failed while reading file {}'.format(node, filename))
                            node = (node - 1 + n) % n
                            count = count - 1
    return resp.json_response(response)



def getFileList():
    return list(FILE_LIST)


# @aiohttp.streamer
# def getFile(writer, filename=None):
#     with open(filename, 'rb') as f:
#         chunk = f.read(2**16)
#         while chunk:
#             yield from writer.write(chunk)
#             chunk = f.read(2**16)
#     f.close()


# # can only add one file at a time 
# async def addFileToNode(filename):
#     hashKey = str(hashlib.sha1(str(filename)).hexdigest())
#     nodeHashList = SN.values()
#     n = len(SN)
#     node = -1
#     for index in range(n):
#         if(nodeHashList(index-1+n%n) < hashKey ) and (hashKey < nodeHashList(index%n)):
#             node = index
#             break
#     if(node == -1) : node = 0
#     count = 3
#     async with aiohttp.ClientSession() as session:
#         while count > 0:
#             nodePort = SN[node]
#             # use 'addFileToNode' as a data provider:
#             async with session.post('https://127.0.0.1:{nodePort}/file/{filename}', data=getFile(filename = filename)) as resp:
#                 print(await resp.text())
#                 print(' file: {} is added to SN: {}  '.format(filename, node))
#                 node = (node - 1 + n) % n
#                 count = count - 1
#         # notify the directory server about adding the file
#         async with session.post('https://127.0.0.1:18888/file/{filename}', data = {filename:getFile(filename = filename)}) as resp:
#             await resp.text()


# # can be a list of filename
# async def readFile(filenames):
#     response = {}
#     async with aiohttp.ClientSession() as session:
#         for filename in filenames:
#             hashKey = str(hashlib.sha1(str(filename)).hexdigest())
#             nodeHashList = SN.values()
#             n = len(SN)
#             node = -1
#             for index in range(n):
#                 if(nodeHashList(index-1+n%n) < hashKey ) and (hashKey < nodeHashList(index%n)):
#                     node = index
#                     break
#             if(node == -1) : node = 0
#             count = 3
#             while count > 0:
#                 nodePort = SN[node]
#                 async with session.get('https://127.0.0.1:{nodePort}/file/{filename}') as resp:
#                     if resp.status == 200:
#                         with open(filename, 'wb') as fd:
#                             while True:
#                                 chunk = await resp.content.read(chunk_size)
#                                 if not chunk:
#                                     break
#                                 fd.write(chunk)
#                         response[filename] = resp.content()
#                         count = 0
#                         break
#                     else:
#                         print(' SN {} failed '.format(node))
#                         node = (node - 1 + n) % n
#                         count = count - 1
#     return resp.json_response(response)
