import aiohttp
import asyncio
import time
import sys
import getopt
import os
import hashlib
import random
from Client import connect, addFile, getFile, getFilelist, readFile

SNport = 20001
OPT_M = -1
OPT_N = -1
OPT_r = 0.5
OPT_f = -1
OPT_d = ''
OPT_verbose = False


async def botmain():
    global OPT_M
    global OPT_N
    global OPT_f
    global OPT_r
    global OPT_d
    global SNport
    global OPT_verbose

    writeNumber = int(OPT_N * OPT_r)
    readNumber = OPT_N - writeNumber
    localFileList = []
    if not os.path.exists(OPT_d):
        os.makedirs(OPT_d)
    for i in range(OPT_M):
        h = hashlib.md5()
        _ = str(random.random())
        h.update(_.encode())
        filename = 'file_' + h.hexdigest() + '.bin'
        with open(os.path.join(OPT_d, filename), 'w') as fout:
            # fout.write(os.urandom(random.randint(1, 256 + 1)))
            fout.write('this is file content for file: {}'.format(filename))
            fout.close()
        localFileList.append(os.path.join(OPT_d, filename))



    while True:
        c_start_time = time.time()
        SNport = await connect()
        c_timecost = time.time() - c_start_time
        print('connect\t[]\t{} ms'.format(c_timecost * 1000))
        # fetch file list
        ls_start = time.time()
        remoteFileList = await getFilelist('global', SNport)
        ls_timecost = time.time() - ls_start
        print('ls\t[]\t{} ms'.format(ls_timecost*1000))

        Tasks = []
        # upload files:
        filesForUpload = random.sample(localFileList, writeNumber)
        for filename in filesForUpload:
            # Tasks.append(addFile(os.path.split(filename)[-1], getFile(filename), SNport))
            start = time.time()
            await addFile(os.path.split(filename)[-1], getFile(filename), SNport)
            timecost = time.time() - start
            print('add\t[{}]\t{} ms'.format(os.path.split(filename)[-1], timecost * 1000))
        # read remote files
        if len(remoteFileList) < readNumber:
            filesForRead = remoteFileList
        else:
            filesForRead = random.sample(remoteFileList, readNumber)
        for filename in filesForRead:
            # Tasks.append(readFile(filename,SNport))
            start = time.time()
            result = await readFile(filename, SNport)
            timecost = time.time() - start
            print('read\t[{}]\t{} ms'.format(filename, timecost * 1000))
            if OPT_verbose:
                print('content of file {} :'.format(filename))
                print(result)
        # done, _ = await asyncio.wait(Tasks)
        # for result in done:
        #     print(result.result())

        await asyncio.sleep(OPT_f)
    #
    #     option = command[0]
    #     if (option == 'addfile'):
    #         filename = command[1]
    #         start = time.time()
    #         await addFile(filename, getFile(filename))
    #         timecost = time.time()-start
    #         print('Time cost for adding file:{} is {} ms'.format(filename, timecost*1000))
    #     elif (option == 'filelist'):
    #         position = 'global'
    #         if len(command) == 2:
    #             position = command[1]
    #         start = time.time()
    #         print(await getFilelist(position))
    #         timecost = time.time()-start
    #         print('Time cost for fetching file list is:{} ms'.format(timecost*1000))
    #     elif (option == 'read'):
    #         filename = command[1]
    #         start = time.time()
    #         content = await readFile(filename)
    #         timecost = time.time()-start
    #         print(content)
    #         print('Time cost for reading file:{} is {} ms'.format(filename,timecost*1000))
    #     elif (option == 'exit'):
    #         sys.exit('exit the system')
    #     else:
    #         print_help()
    # return


def print_help():
    print("python3 ClientBot.py [options]\n"
          "\t-h show this help\n"
          "\t-d directory for generating files to upload\n"
          "\t-M how many files this bot is going to generate and upload\n"
          "\t-N how many requests this bot is going to send in every period\n"
          "\t-r write/total ratio (example: -r 0.25 means 0.25 write 0.75read)\n"
          "\t-f the frequency to send request in seconds")
    return


# options parser
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hd:M:N:r:f:v')
    # print(opts)
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for (opt, arg) in opts:
    if opt == '-h':
        print_help()
        sys.exit()
    elif opt == '-d':
        OPT_d = arg
    elif opt == '-M':
        OPT_M = int(arg)
    elif opt == '-N':
        OPT_N = int(arg)
    elif opt == '-r':
        OPT_r = float(arg)
    elif opt == '-f':
        OPT_f = int(arg)
    elif opt == '-v':
        OPT_verbose = True

if -1 in [OPT_M, OPT_N, OPT_f] or OPT_d == '':
    print([OPT_M, OPT_N, OPT_f, OPT_d, OPT_r])
    print_help()
    sys.exit(2)

asyncio.run(botmain())
