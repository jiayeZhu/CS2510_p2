import asyncio, aiohttp
import hashlib
import json
import os
import random

SN = {1: 20001, 2: 20002, 3: 20003, 4: 20004, 5: 20005, 6: 20006, 7: 20007, 8: 20008}  # nodeId : port
ALIVE_SN = []
currentNode = 1
currentPort = 20001
server = "127.0.0.1:8888"
folder = 'SN{}_storage'.format(currentNode)
FILE_LIST = set()
FIRST = True
UP_TO_DATE=True


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


def findSection(hashkey):
    return hashkey // (2 ** 157)  # 0~7


def findLocation(hashKey):
    global ALIVE_SN
    section = findSection(hashKey)
    targetList = []
    pointer = (section + 1) % 8 + 1
    for i in range(8):
        if pointer in ALIVE_SN:
            targetList.append(pointer)
        if len(targetList) == 3:
            break
        else:
            pointer = pointer % 8 + 1
    return targetList
    # n = len(SN)
    # division = int(((2**160)-1)/n)
    # for index in range(n):
    #     if(index * division < hashKey ) and (hashKey< (index + 1) * division):
    #         nodeID = index + 1
    #         break
    # targetList = list(map(lambda x: (x + len(SN)) % len(SN), [nodeID, nodeID-1, nodeID-2]))
    # targetList = [8 if i == 0 else i for i in targetList]
    # return targetList


# can only add one file at a time 
async def addFileToNode(filename, content):
    # print('adding : ', filename)
    if (filename in FILE_LIST):
        pass
    else:
        # find where should this file stored
        hashKey = computeHash(filename)
        targetList = findLocation(hashKey)
        # print('target nodes are : ', targetList)
        # Forward the request
        async with aiohttp.ClientSession() as session:
            tasks = []
            for node in targetList:
                if (node == currentNode):
                    storeFile(filename, content)
                    FILE_LIST.add(filename)
                else:
                    # print('the request is : http://127.0.0.1:{}/file/{}'.format(SN[node], filename)  )
                    nodePort = SN[node]
                    tasks.append(session.post('http://127.0.0.1:{}/file/{}'.format(nodePort, filename), data=content))
                # print(' file: {} is added to SN: {}  '.format(filename, node))
            if len(tasks) != 0:
                await asyncio.wait(tasks)
            # notify the directory server about adding the file
            async with session.post('http://127.0.0.1:8888/file/{}'.format(filename)) as resp:
                await resp.read()


# invoked by the requester to read the file by provide filename.
async def readFile(filename):
    # print('reading : ', filename)
    response = None
    hashKey = computeHash(filename)
    targetList = findLocation(hashKey)
    # print('target nodes are : ', targetList)
    # if the file should be stored in the current node
    if (currentNode in targetList):
        if (filename in FILE_LIST):
            try:
                f = open('{}/{}'.format(folder, filename), 'rb')
                response = f.read()
            except Exception as e:
                response = None
            finally:
                if f:
                    f.close()
        else:
            if targetList.index(currentNode) == 0:
                response = None
            else:
                async with aiohttp.ClientSession() as session:
                    nodeId = targetList[targetList.index(currentNode) - 1]
                    nodePort = SN[nodeId]
                    result = await session.get('http://127.0.0.1:{}/file/{}'.format(nodePort, filename))
                    if result.status != 200:
                        response = None
                    else:
                        content = await result.read()
                        storeFile(filename, content)
                        FILE_LIST.add(filename)
                        response = content
    # if the file is not stored in the current node
    else:
        async with aiohttp.ClientSession() as session:
            # forward the request
            nodeID = random.sample(targetList, 1)[0]
            # print('file {} is stored at node: {}'.format(filename, nodeID))
            nodePort = SN[nodeID]
            # print("the request is : http://127.0.0.1:{}/file/{}".format(nodePort, filename))
            async with session.get('http://127.0.0.1:{}/file/{}'.format(nodePort, filename)) as resp:
                response = await resp.read()
                print(await resp.read())
    return response
    # print(response)
    # return  str(response, encoding='utf-8')


def getFileList():
    return list(FILE_LIST)


async def fetchFile(targertAddr, filename):
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.get('http://127.0.0.1:{}/file/{}'.format(targertAddr, filename))
            if result.status != 404:
                content = await result.read()
                storeFile(filename, content)
            return
        except Exception as e:
            pass
            # print('fetchFile failed')
        # return session.get('http://{}/file/{}'.format(targertAddr, filename))


async def SNbeat():
    global server
    global ALIVE_SN
    global FIRST
    global SN
    global FILE_LIST
    global UP_TO_DATE
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(1)
        async with aiohttp.ClientSession() as session:
            SNID = currentNode - 1
            try:
                result = await session.put('http://{}/hb/{}'.format(server, SNID))
                result = await result.json()
                if ALIVE_SN != result['alive_sn_list']:
                    ALIVE_SN = result['alive_sn_list']
                    UP_TO_DATE = False
                if FIRST or not UP_TO_DATE:
                    result = await session.get('http://{}/filelist'.format(server))
                    result = await result.json()
                    systemFileList = result['fileList']
                    if len(systemFileList) != 0:
                        tasks = []
                        for file in systemFileList:
                            if file in FILE_LIST:
                                continue
                            hash = computeHash(file)
                            locations = findLocation(hash)
                            if currentNode not in locations:
                                continue
                            randomTarget = random.sample(locations, 1)[0]
                            tasks.append(fetchFile(SN[randomTarget], file))
                        if len(tasks) > 0:
                            await asyncio.wait(tasks)
                    FIRST = False
                    UP_TO_DATE = True
            except Exception as e:
                print('SN {} failed when beat() with exception'.format(currentNode))
                print(e)
