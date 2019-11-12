import asyncio
import aiohttp
import random

HEARTBEAT_TIMEOUT = 5
SN_STATUS = list((HEARTBEAT_TIMEOUT,) * 8)
FILE_LIST = {}
SN_ADDR_LIST = ['127.0.0.1:20001','127.0.0.1:20002','127.0.0.1:20003','127.0.0.1:20004','127.0.0.1:20005','127.0.0.1:20006','127.0.0.1:20007','127.0.0.1:20008']


def countdown(x):
    if x == 0:
        return 0
    else:
        return x - 1


async def beat():
    global SN_STATUS
    while True:
        await asyncio.sleep(1)
        SN_STATUS = list(map(countdown, SN_STATUS))
        async with aiohttp.ClientSession() as session:
            await session.put('http://127.0.0.1:18888/sync', json=getState())


async def connect():
    candidates = [idx for idx in range(8) if SN_STATUS[idx] is not 0]
    return SN_ADDR_LIST[random.sample(candidates,1)[0]] if len(candidates) is not 0 else 'N/A'


def getFileList():
    return list(FILE_LIST)


# files should be a list of filename
def addFileToFileList(files):
    FILE_LIST.update(files)


def getStorageNodeStatus(id=-1):
    if id == -1:
        return SN_STATUS
    else:
        return SN_STATUS[id]


def refreshStorgateNodeStatus(id):
    SN_STATUS[id] = HEARTBEAT_TIMEOUT


def getState():
    return {'FILE_LIST': list(FILE_LIST), 'SN_STATUS': SN_STATUS}


def setState(state):
    global FILE_LIST
    global SN_STATUS
    global ret
    FILE_LIST = set(state['FILE_LIST'])
    SN_STATUS = state['SN_STATUS']
