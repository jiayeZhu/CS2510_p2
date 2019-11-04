from aiohttp import web
from routers import dnsRoutes

app = web.Application()
app.add_routes(dnsRoutes)
web.run_app(app, port=8888)
