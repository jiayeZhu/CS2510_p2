from aiohttp import web
import asyncio
import logging
from routers.SNRouter import routes



app = web.Application()
# app.on_startup.append()
# app.on_cleanup.append()
logging.basicConfig(level=logging.DEBUG)
app.add_routes(routes)
web.run_app(app, port=20001, access_log_format='%a %t %r %s %b %Tf') #TODO