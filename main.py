import logging
import re

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis_worker import r, check_availability
from starlette.requests import Request
from fastapi.responses import JSONResponse


NOT_AUTHORIZATION_PATTERNS = [
    "/",
    "/ping",
    "/docs",
    "/openapi.json",
    "/users/login"
]


app = FastAPI(
    title="Black Wall Group Test Assignment"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)


@app.middleware("http")
async def add_authorization(request: Request,  call_next):
    token = ''
    if not any([re.fullmatch(pattern, request.url.path) for pattern in NOT_AUTHORIZATION_PATTERNS]):
        token = request.cookies.get("access_token")
        if not token or token != "token":
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'message': "invalid token"})

    response = await call_next(request)
    if token:
        response.set_cookie("access_token", token)

    return response


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    logging.warning(f"Redis available: {await check_availability()}")


if __name__ == "__main__":
    uvicorn.run(app="src.api:app", reload=True)
