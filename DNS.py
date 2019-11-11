from aiohttp import web
from routers import dnsRoutes
import logging
from services import setDSList
import sys
import getopt


def print_help():
    print("python3 DNS.py [options]\n"
          "\t-h show this help\n"
          "\t--DSLIST=\"DS0ADDR:PORT,DS1ADDR:PORT,DS2ADDR:PORT\"")
    return


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
logging.basicConfig(level=logging.DEBUG)
app.add_routes(dnsRoutes)
web.run_app(app, port=8888, access_log_format='%a %t %r %s %b %Tf')
