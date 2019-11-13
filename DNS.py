from aiohttp import web
from routers import dnsRoutes
import logging
from services import setDSList, DNSbeat
import sys
import getopt
import asyncio


def print_help():
    print("python3 DNS.py [options]\n"
          "\t-h show this help\n"
          "\t--DSLIST=\"DS0ADDR:PORT,DS1ADDR:PORT,DS2ADDR:PORT\"")
    return


async def start_background_tasks(app):
    app['heart_beater'] = asyncio.create_task(DNSbeat())


async def cleanup_background_tasks(app):
    app['heart_beater'].cancel()
    await app['heart_beater']


# options parser
try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['DSLIST='])
    # print(opts)
except getopt.GetoptError:
    print_help()
    sys.exit(2)
for (opt, arg) in opts:
    if opt == '-h':
        print_help()
        sys.exit()
    elif opt == '--DSLIST':
        setDSList(arg.split(','))

app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
logging.basicConfig(level=logging.DEBUG)
app.add_routes(dnsRoutes)
web.run_app(app, port=8888, access_log_format='%a %t %r %s %b %Tf')
