import asyncio
import aiohttp
import random

HEARTBEAT_TIMEOUT = 3
SN_STATUS = list((HEARTBEAT_TIMEOUT,) * 8)
FILE_LIST = set()
SN_ADDR_LIST = ['127.0.0.1:20001', '127.0.0.1:20002', '127.0.0.1:20003', '127.0.0.1:20004', '127.0.0.1:20005',
                '127.0.0.1:20006', '127.0.0.1:20007', '127.0.0.1:20008']
PORT = 18888
PEERS = []
DNS_addr = '127.0.0.1:8888'
FIRST = True
RECOVERYLIST = []


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


async def sync(hbsync=False, hbid=-1):
    global PEERS
    global DNS_addr
    async with aiohttp.ClientSession() as session:
        DSID = getDSPORT() - 18888
        try:
            peers = await session.get('http://' + DNS_addr + '/ds/list/alive')
            peers = await peers.json()
            setDSPeers(peers['ds_list'])
            jsonData = getDSState()
            if hbsync:
                jsonData['hbsync'] = True
                jsonData['hbid'] = hbid
            else:
                jsonData['hbsync'] = False
            tasks = [session.put('http://{}/sync'.format(addr), json=jsonData) for addr in PEERS if
                     addr != '127.0.0.1:{}'.format(getDSPORT())]
            if len(tasks) != 0:
                await asyncio.wait(tasks)
        except Exception as e:
            pass
            # print('DS {} failed when sync()'.format(DSID))
            # print(e)


async def DSbeat():
    global SN_STATUS
    global DNS_addr
    global PEERS
    global FIRST
    await asyncio.sleep(1)
    if FIRST:
        async with aiohttp.ClientSession() as session:
            try:
                peers = await session.get('http://' + DNS_addr + '/ds/list/alive')
                peers = await peers.json()
                if len(peers['ds_list']) == 0:  # no alive nodes, state is clean
                    FIRST = False
                else:
                    state = await session.get('http://{}/sync'.format(peers['ds_list'][0]))
                    state = await state.json()
                    FIRST = False
            except:
                pass
    while True:
        await asyncio.sleep(1)
        SN_STATUS = list(map(countdown, SN_STATUS))
        async with aiohttp.ClientSession() as session:
            DSID = getDSPORT() - 18888
            try:
                await session.put('http://{}/ds/hb/{}'.format(DNS_addr, DSID))
            except:
                pass
                # print('DS {} failed when beat()'.format(DSID))
            # await sync()


async def connect():
    candidates = [idx for idx in range(8) if SN_STATUS[idx] is not 0]
    return SN_ADDR_LIST[random.sample(candidates, 1)[0]] if len(candidates) is not 0 else 'N/A'


def getFileList():
    return list(FILE_LIST)


# files should be a list of filename
async def addFileToFileList(files):
    # print(files)
    FILE_LIST.update(files)
    await sync()


def getStorageNodeStatus(id=-1):
    if id == -1:
        return SN_STATUS
    else:
        return SN_STATUS[id]


def setStorageNodeStatue(id):
    SN_STATUS[id] = HEARTBEAT_TIMEOUT


async def refreshStorgateNodeStatus(id):
    global SN_STATUS
    global RECOVERYLIST
    if SN_STATUS[id] == 0 and id not in RECOVERYLIST:
        RECOVERYLIST.append(id)
    else:
        SN_STATUS[id] = HEARTBEAT_TIMEOUT
        if id in RECOVERYLIST:
            RECOVERYLIST.remove(id)
    await sync(True, id)


def getDSState():
    return {'FILE_LIST': list(FILE_LIST), 'SN_STATUS': SN_STATUS}


def setState(state):
    global FILE_LIST
    global SN_STATUS
    FILE_LIST = set(state['FILE_LIST'])
    SN_STATUS = state['SN_STATUS']
