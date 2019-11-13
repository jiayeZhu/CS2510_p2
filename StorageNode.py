from aiohttp import web
import asyncio
import logging
import getopt
import sys
import os
from routers.SNRouter import routes


PORT = 20001
server = "127.0.0.1:8888"
folder = 'SN1_storage'

def print_help():
    print("python3 StorageNode.py [options]\n"
          "\t-h show this help\n"
          "\t-p <listening to this port>\n"
          "\t--servers=\"ADDR:PORT\""
          "\t-d store files in this folder\n")
    return

# options parser
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hp:d', 'servers=')
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for (opt, arg) in opts:
    if opt == '-h':
        print_help()
        sys.exit()
    elif opt == '-p':
        PORT = int(arg)
    elif opt == '--servers':
        server = str(arg)
    elif opt == '-d':
        folder = os.getcwd()[:-len(arg)] + '{}\\'.format(arg)
        os.makedirs(folder)


app = web.Application()
# app.on_startup.append()
# app.on_cleanup.append()
logging.basicConfig(level=logging.DEBUG)
app.add_routes(routes)
web.run_app(app, port=PORT, access_log_format='%a %t %r %s %b %Tf')