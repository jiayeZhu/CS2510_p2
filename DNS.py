from aiohttp import web
from routers import dnsRoutes
import logging


app = web.Application()
logging.basicConfig(level=logging.DEBUG)
app.add_routes(dnsRoutes)
web.run_app(app, port=8888, access_log_format='%a %t %r %s %b %Tf')
