import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis_worker import r, check_availability

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


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    print(f"Redis available: {await check_availability()}")


if __name__ == "__main__":
    uvicorn.run(app="src.api:app", reload=True)
