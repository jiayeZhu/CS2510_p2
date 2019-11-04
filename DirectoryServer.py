from aiohttp import web

routes = web.RouteTableDef()


app = web.Application()
app.add_routes(routes)
web.run_app(app)
