from src.api.users.router import router as users_router
from src.api.symbols.router import router as symbols_router

all_routers = [
    users_router,
    symbols_router
]
