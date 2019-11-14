import aiohttp
import asyncio
import re
import json
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
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.get('http://127.0.0.1:8888/connect')
            response = (await result.read()).decode("utf-8") 
        except Exception as e:
            print(e)
    SNport = re.findall(r"\d*",response.split(':')[-1])
    return [i for i in SNport if i != ''][0]

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
    if(data == None):
        return
        # print('No such file : ', filename)
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.post('http://127.0.0.1:{}/file/{}'.format(SNport, filename), data=data)
            if(result.status == 200):
                print('{} added successfully'.format(filename))
        except Exception as e:
            print(e)

async def getFilelist():
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.get('http://127.0.0.1:8888/filelist')
            # print(await result.read())
            response = (await result.read()).decode("utf-8")
            # print('the filelist : ',json.loads(response)['fileList:'])
            filelist = json.loads(response)['fileList:']
            if (filelist == []):
                return ('No file is stored in the current system')
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
    SNport = await connect()
    print("connected to storage node : ", SNport)
    while True:
        command = input(">> ").split()
        option = command[0]
        if(option == 'addfile'):
            filename = command[1]
            await addFile(filename, getFile(filename))
        elif(option == 'filelist'):
            print(await getFilelist())
        elif(option == 'read'):
            filename = command[1]
            content = await readFile(filename)
            print(content)
        elif(option == 'exit'):
            sys.exit('exit the system')
        else:
            print_help()
    return



asyncio.run(main())