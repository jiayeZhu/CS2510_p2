from aiohttp import web
from routers import dsRoutes
import asyncio
import logging
from services.DSServices import beat


async def start_background_tasks(app):
    app['heart_beater'] = asyncio.create_task(beat())


async def cleanup_background_tasks(app):
    app['heart_beater'].cancel()
    await app['heart_beater']


app = web.Application()
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
logging.basicConfig(level=logging.DEBUG)
app.add_routes(dsRoutes)
web.run_app(app, port=18888, access_log_format='%a %t %r %s %b %Tf')
