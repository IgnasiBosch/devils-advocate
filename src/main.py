from fastapi import FastAPI

from src.db import Base, get_engine
from src.routes import router


def get_app() -> FastAPI:
    Base.metadata.create_all(get_engine())
    app = FastAPI()
    app.include_router(router)

    return app


app = get_app()
