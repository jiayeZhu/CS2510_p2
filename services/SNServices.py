import asyncio, aiohttp
import hashlib
import json
import os
import random


SN = {1:20001, 2:20002, 3:20003, 4:20004, 5:20005, 6:20006, 7:20007, 8:20008}  # nodeId : port
currentNode = 1
currentPort = 20001
server = "127.0.0.1:8888"
folder = 'SN{}_storage'.format(currentNode)
FILE_LIST = {}


async def SNbeat():
    global server
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(1)
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            SNID = currentNode-1
            try:
                await session.put('http://{}/hb/{}'.format(server, SNID))
            except Exception as e:
                print('SN {} failed when beat() with exception'.format(SNID))
                print(e)


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
    targetList = list(map(lambda x: (x + len(SN)) % len(SN), [nodeID, nodeID-1, nodeID-2]))
    targetList = [8 if i == 0 else i for i in targetList]
    return targetList


# can only add one file at a time 
async def addFileToNode(filename, content):
    print('adding : ',filename)
    if(filename in FILE_LIST):
        pass
    else:
        # find where should this file stored
        hashKey = computeHash(filename)
        targetList = findLocation(hashKey)
        print('target nodes are : ', targetList)
        # Forward the request
        async with aiohttp.ClientSession() as session:
            for node in targetList:
                if(node == currentNode):
                    storeFile(filename, content)
                    FILE_LIST.add(filename)
                else:
                    print('the request is : http://127.0.0.1:{}/file/{}'.format(SN[node], filename)  )
                    nodePort = SN[node]
                    async with session.post('http://127.0.0.1:{}/file/{}'.format(nodePort, filename), data=content) as resp:
                        print(await resp.read())
                print(' file: {} is added to SN: {}  '.format(filename, node))
            # notify the directory server about adding the file
            async with session.post('http://127.0.0.1:8888/file/{}'.format(filename), data = filename) as resp:
                await resp.read()
        

# invoked by the requester to read the file by provide filename.
async def readFile(filename):
    print('reading : ', filename)
    response = None
    hashKey = computeHash(filename)
    targetList = findLocation(hashKey)
    print('target nodes are : ', targetList)
    # if the file should be stored in the current node
    if (currentNode in targetList):
        if (filename in FILE_LIST):
            try:
                f = open('{}/{}'.format(folder, filename), 'rb')
                response = f.read()
            finally:
                if f:
                    f.close() 
        else: response = None
    # if the file is not stored in the current node
    else:
        async with aiohttp.ClientSession() as session:
            # forward the request
            nodeID = random.sample(targetList,1)[0]
            print('file {} is stored at node: {}'.format(filename, nodeID))
            nodePort = SN[nodeID]
            print("the request is : http://127.0.0.1:{}/file/{}".format(nodePort, filename))
            async with session.get('http://127.0.0.1:{}/file/{}'.format(nodePort, filename)) as resp:
                response = await resp.read()
                print(await resp.read())
    return response
    # print(response)
    # return  str(response, encoding='utf-8')


def getFileList():
    return list(FILE_LIST)
