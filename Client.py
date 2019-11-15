import aiohttp
import asyncio
import time
import sys

SNport = 20001


def print_help():
    print("\nhelp : show help \n"
          "addfile [filename] : add a file to the system\n"
          "filelist : check the list of files in the storage system\n"
          "read [filename] : read the target file\n"
          "exit : exit the system\n")

    return


async def connect():
    global SNport
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.get('http://127.0.0.1:8888/connect')
            response = await result.json()
            SNport = int(response['SN'].split(':')[-1])
            return SNport
        except Exception as e:
            print(e)


def getFile(filename):
    try:
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        return data
    except Exception as e:
        print(e)
        return None


async def addFile(filename, data):
    if (data == None):
        return
        # print('No such file : ', filename)
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.post('http://127.0.0.1:{}/file/{}'.format(SNport, filename), data=data)
            if (result.status == 200):
                print('{} added successfully'.format(filename))
        except Exception as e:
            print(e)


async def getFilelist(position):
    global SNport
    async with aiohttp.ClientSession() as session:
        try:
            addr = 'http://127.0.0.1:8888/filelist' if position == 'global' else 'http://127.0.0.1:{}/filelist'.format(SNport)
            result = await session.get(addr)
            # print(await result.read())
            response = await result.json()
            # print('the filelist : ',json.loads(response)['fileList:'])
            filelist = response['fileList']
            if (filelist == []):
                return 'No file is stored in the current system' if position == 'global' else 'No file is stored in ' \
                                                                                              'the current node'
            return (filelist)

        except Exception as e:
            print(e)


async def readFile(filename):
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.get('http://127.0.0.1:{}/file/{}'.format(SNport, filename))
            # print(result.status)
            response = (await result.read()).decode("utf-8")
            return response
        except Exception as e:
            print(e)


async def main():
    print_help()
    c_start_time = time.time()
    await connect()
    c_timecost = time.time()-c_start_time
    print("connected to storage node : ", SNport)
    print('Time cost for connecting is {} ms'.format(c_timecost*1000))
    while True:
        command = input(">> ").split()
        option = command[0]
        if (option == 'addfile'):
            filename = command[1]
            start = time.time()
            await addFile(filename, getFile(filename))
            timecost = time.time()-start
            print('Time cost for adding file:{} is {} ms'.format(filename, timecost*1000))
        elif (option == 'filelist'):
            position = 'global'
            if len(command) == 2:
                position = command[1]
            start = time.time()
            print(await getFilelist(position))
            timecost = time.time()-start
            print('Time cost for fetching file list is:{} ms'.format(timecost*1000))
        elif (option == 'read'):
            filename = command[1]
            start = time.time()
            content = await readFile(filename)
            timecost = time.time()-start
            print(content)
            print('Time cost for reading file:{} is {} ms'.format(filename,timecost*1000))
        elif (option == 'exit'):
            sys.exit('exit the system')
        else:
            print_help()
    return


asyncio.run(main())
