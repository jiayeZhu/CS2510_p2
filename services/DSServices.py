import asyncio

HEARTBEAT_TIMEOUT = 5
SN_STATUS = list((HEARTBEAT_TIMEOUT,) * 8)
FILE_LIST = {}


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
