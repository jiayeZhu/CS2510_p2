from aiohttp import web
import logging

routes = web.RouteTableDef()


@routes.get('/')
async def root(request):
    return web.json_response({'suc': True, 'addr': 'STATIC'})


@routes.post('/')
async def a(request):
    return web.json_response({'msg': 'post at root'})


@routes.post('/{any}')
async def b(request):
    result = await request.json()
    print(result)
    return web.json_response({'msg': 'post at /{any}'})

@routes.get('/file/{any}')
async def filehandler(request):
    return web.Response(text='a')

app = web.Application()
logging.basicConfig(level=logging.DEBUG)
app.add_routes(routes)
web.run_app(app, port=18888, access_log_format='%a %t %r %s %b %Tf')
