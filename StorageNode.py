from aiohttp import web
import asyncio
import logging
import getopt
import sys
import os
from routers.SNRouter import routes
from services.SNServices import setPort, setServer, setFolder, SNbeat


PORT = 20001

async def start_background_tasks(app):
    app['heart_beater'] = asyncio.create_task(SNbeat())


async def cleanup_background_tasks(app):
    app['heart_beater'].cancel()
    await app['heart_beater']


def print_help():
    print("python3 StorageNode.py [options]\n"
          "\t-h show this help\n"
          "\t-p <listening to this port>\n"
          "\t--servers=\"ADDR:PORT\"\n"
          "\t-d store files in this folder\n")
    return

# options parser
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hp:d:', 'servers=')
    # print(opts)
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for (opt, arg) in opts:
    if opt == '-h':
        print_help()
        sys.exit()
    elif opt == '-p':
        PORT = int(arg)
        setPort(int(arg))
    elif opt == '--servers':
        setServer(str(arg))
    elif opt == '-d':
        setFolder(str(arg))


app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
logging.basicConfig(level=logging.DEBUG)
app.add_routes(routes)
web.run_app(app, port=PORT, access_log_format='%a %t %r %s %b %Tf')