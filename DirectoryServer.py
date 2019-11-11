from aiohttp import web
from routers import dsRoutes
import asyncio
import logging
from services.DSServices import beat
import getopt
import sys

PORT = 18888
PEERS = []

async def start_background_tasks(app):
    app['heart_beater'] = asyncio.create_task(beat())


async def cleanup_background_tasks(app):
    app['heart_beater'].cancel()
    await app['heart_beater']


def print_help():
    print("python3 DirectoryServer.py [options]\n"
          "\t-h show this help\n"
          "\t-p <listening to this port>\n"
          "\t--peers=\"DS1ADDR:PORT,DS2ADDR:PORT\"")
    return


# options parser
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hp:', ['peers='])
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
    elif opt == '--peers':
        PEERS = arg.split(',')

if len(PEERS) is not 2:
    print_help()
    sys.exit()

app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
logging.basicConfig(level=logging.DEBUG)
app.add_routes(dsRoutes)
web.run_app(app, port=PORT, access_log_format='%a %t %r %s %b %Tf')
