from aiohttp import web
from routers import dsRoutes
import asyncio
import logging
from services import DSbeat, setDSPORT, setDNSaddr
import getopt
import sys

port = 18888


async def start_background_tasks(app):
    app['heart_beater'] = asyncio.create_task(DSbeat())


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
    opts, args = getopt.getopt(sys.argv[1:], 'hp:', ['server='])
    # print(opts)
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for (opt, arg) in opts:
    if opt == '-h':
        print_help()
        sys.exit()
    elif opt == '-p':
        setDSPORT(int(arg))
        port = int(arg)
    elif opt == '--server':
        setDNSaddr(arg)


app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
logging.basicConfig(level=logging.DEBUG)
app.add_routes(dsRoutes)
web.run_app(app, port=port, access_log_format='%a %t %r %s %b %Tf')
