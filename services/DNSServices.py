import asyncio
import random
HEARTBEAT_TIMEOUT=4
DS_list = ['127.0.0.1:18888', '127.0.0.1:18889', '127.0.0.1:18890']
DS_STATUS = list((HEARTBEAT_TIMEOUT,) * 3)
ALIVE_DS = []
def countdown(x):
    if x == 0:
        return 0
    else:
        return x - 1


def getOneDS():
    global ALIVE_DS
    # aliveDS = [DS_list[i]for i in range(3) if DS_STATUS[i] != 0]
    if len(ALIVE_DS) == 0:
        return DS_list[0]
    else:
        return random.sample(ALIVE_DS, 1)[0]


def getDSList(aliveOnly=False):
    if not aliveOnly:
        return DS_list
    else:
        return [DS_list[i] for i in range(3) if DS_STATUS[i] is not 0]


def regOneDS(addr):
    DS_list.append(addr)


def setDSList(dsList):
    global DS_list
    DS_list = dsList


def refreshDirectoryServerStatus(id):
    global DS_STATUS
    DS_STATUS[id] = HEARTBEAT_TIMEOUT


async def DNSbeat():
    global DS_STATUS
    global ALIVE_DS
    while True:
        await asyncio.sleep(1)
        DS_STATUS = list(map(countdown, DS_STATUS))
        ALIVE_DS = [DS_list[i]for i in range(3) if DS_STATUS[i] != 0]
        # print(DS_STATUS)