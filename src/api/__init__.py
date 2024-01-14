from src.api.index import app
from .symbols import router

app.include_router(router)

__all__ = ["app"]
