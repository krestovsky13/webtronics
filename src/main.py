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
    )

    conf_init(app)
    init_router(app)

    return app


app = start_application()
