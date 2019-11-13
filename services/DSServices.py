import asyncio
import aiohttp
import random

HEARTBEAT_TIMEOUT = 5
SN_STATUS = list((HEARTBEAT_TIMEOUT,) * 8)
FILE_LIST = {}
SN_ADDR_LIST = ['127.0.0.1:20001', '127.0.0.1:20002', '127.0.0.1:20003', '127.0.0.1:20004', '127.0.0.1:20005',
                '127.0.0.1:20006', '127.0.0.1:20007', '127.0.0.1:20008']
PORT = 18888
PEERS = []
DNS_addr = '127.0.0.1:8888'


def setDSPORT(port):
    global PORT
    PORT = port


def getDSPORT():
    global PORT
    return PORT


def setDSPeers(peers):
    global PEERS
    PEERS = peers


def setDNSaddr(addr):
    global DNS_addr
    DNS_addr = addr


def countdown(x):
    if x == 0:
        return 0
    else:
        return x - 1


async def DSbeat():
    global SN_STATUS
    global DNS_addr
    global PEERS
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(1)
        SN_STATUS = list(map(countdown, SN_STATUS))
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            DSID = getDSPORT() - 18888
            try:
                await session.put('http://{}/ds/hb/{}'.format(DNS_addr, DSID))
                peers = await session.get('http://' + DNS_addr + '/ds/list/alive')
                peers = await peers.json()
                setDSPeers(peers['ds_list'])
                await asyncio.wait([session.put('http://' + addr + '/sync', json=getState()) for addr in PEERS])
            except:
                print('DS {} failed when beat()'.format(DSID))



async def connect():
    candidates = [idx for idx in range(8) if SN_STATUS[idx] is not 0]
    return SN_ADDR_LIST[random.sample(candidates, 1)[0]] if len(candidates) is not 0 else 'N/A'


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
