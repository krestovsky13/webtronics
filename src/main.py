from fastapi import FastAPI

from api.route import init_router
from core.config import settings


def conf_init(app):
    """
    Настройки для dev версии
    """
    if not settings.DEBUG:
        app.docs_url = None
        app.redoc_url = None
        app.debug = False


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        # on_startup=[
        #     db.init_tables,
        # ]
    )

    conf_init(app)
    init_router(app)

    return app


app = start_application()

# async def logs(cont, name):
#     conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
#     async with aiohttp.ClientSession(connector=conn) as session:
#         async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
#             async for line in resp.content:
#                 print(name, line)
