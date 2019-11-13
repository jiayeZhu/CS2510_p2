import asyncio, aiohttp
import hashlib
import json
import os



SN = {1:20001, 2:20002, 3:20003, 4:20004, 5:20005, 6:20006, 7:20007, 8:20008}  # nodeId : port
currentNode = 1
currentPort = 20001
server = "127.0.0.1:8888"
folder = 'SN{}_storage'.format(currentNode)
FILE_LIST = {}


def setPort(port):
    global currentPort, currentNode
    currentPort = port
    currentNode = int(str(currentPort)[-1])
    print('port : {}   nodeID : {}'.format(currentPort, currentNode))

def setServer(serveraddr):
    global server
    server = serveraddr
    print('server : {}'.format(server))

def setFolder(folderName):
    global folder, FILE_LIST
    folder = folderName
    if not os.path.exists(folder):
        os.makedirs(folder)
    # os.makedirs('{}'.format(folder))
    FILE_LIST = set(os.listdir(folder))
    print('folder : {}   FILE_LIST : {}'.format(folder, FILE_LIST))


def computeHash(x):
    return int.from_bytes(hashlib.sha1(str(x).encode('utf-8')).digest(), 'big')


def storeFile(filename, fileContent):
    with open('{}/{}'.format(folder, filename), 'wb') as f:
        f.write(fileContent)


def findLocation(hashKey):
    n = len(SN)
    division = int(((2**160)-1)/n)
    for index in range(n):
        if(index * division < hashKey ) and (hashKey< (index + 1) * division):
            nodeID = index + 1
            break
    return nodeID


# can only add one file at a time 
async def addFileToNode(filename, content):
    print(filename)
    if(filename in FILE_LIST):
        pass
    else:
        # find where should this file stored
        hashKey = computeHash(filename)
        nodeID = findLocation(hashKey)
        print('this file should be stored at node {}, currentNode is {}'.format(nodeID, currentNode))
        # Forward the request
        count = 3
        n = len(SN)
        async with aiohttp.ClientSession() as session:
            while count > 0:
                print('count :', count)
                if(nodeID == currentNode):
                    storeFile(filename, content)
                    FILE_LIST.add(filename)
                else:
                    print('the request is : https://127.0.0.1:{}/file/{}'.format(SN[nodeID], filename)  )
                    nodePort = SN[nodeID]
                    async with session.post('https://127.0.0.1:{}/file/{}'.format(nodePort, filename), data=content) as resp:
                        print(await resp.status)
                print(' file: {} is added to SN: {}  '.format(filename, nodeID))
                nodeID = (nodeID - 1 + n) % n
                if nodeID == 0 : nodeID = 8
                count = count - 1
            # notify the directory server about adding the file
            async with session.post('https://127.0.0.1:8888/file/{}'.format(filename), data = filename) as resp:
                await resp.status
        

# invoked by the requester to read the file by provide filename.
async def readFile(filename):
    print(filename)
    # if the file is stored in the current node
    if filename in FILE_LIST:
        try:
            f = open('{}/{}'.format(folder, filename), 'rb')
            response = f.read()
        finally:
            if f:
                f.close() 
    # if the file is not stored in the current node
    else:
        async with aiohttp.ClientSession() as session:
            # find out where this file stored
            hashKey = computeHash(filename)
            nodeID = findLocation(hashKey)
            count = 3
            n = len(SN)
            print('file {} is stored at node: {}'.format(filename, nodeID))
            while count > 0:
                nodePort = SN[nodeID]
                print("the request is : http://127.0.0.1:{}/file/{}".format(nodePort, filename))
                async with session.get('http://127.0.0.1:{}/file/{}'.format(nodePort, filename)) as resp:
                    response = await resp.read()
                    if resp.status == 200:
                        break
                    else:
                        print(' SN {} fail to read file {}'.format(nodeID, filename))
                        nodeID = (nodeID - 1 + n) % n
                        count = count - 1
    return response
    # print(response)
    # return  str(response, encoding='utf-8')


def getFileList():
    return list(FILE_LIST)


# # can be a list of filename
# async def readFile(filenames):
#     response = {}   # dict{filename: fileContent}
#     for filename in filenames:
#         # if the file is stored in the current node
#         if filename in FILE_LIST:
#             try:
#                 f = open('../SN{}_storage/{}'.format(currentNode, filename), 'rb')
#                 data = f.read() 
#                 response[filename] = data
#             finally:
#                 if f:
#                     f.close() 
#         # if the file is not stored in the current node
#         else:
#             async with aiohttp.ClientSession() as session:
#                 # find out where this file stored
#                 hashKey = str(hashlib.sha1(str(filename)).hexdigest())
#                 nodeID = findLocation(hashKey)
#                 count = 3
#                 n = len(SN)
#                 while count > 0:
#                     nodePort = SN[node]
#                     async with session.get('https://127.0.0.1:{nodePort}/file/{filename}') as resp:
#                         if resp.status == 200:
#                             msg = json.loads(resp.json())
#                             response.update(msg)
#                             break
#                         else:
#                             print(' SN {} fail to read file {}'.format(node, filename))
#                             node = (node - 1 + n) % n
#                             count = count - 1
#     # return resp.json_response(response)
#     # return response
#     return json.dumps(response)