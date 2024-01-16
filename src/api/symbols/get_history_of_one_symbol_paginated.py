from .router import router
from src.schemas.request import SymbolsEnum
from src.api.dependencies import UOWDep
from src.services.currency_pairs import CurrencyPairsService
from fastapi_pagination import Page
from fastapi_cache.decorator import cache

from src.schemas.currency_pairs import CurrencyPairTime


@router.get(
    "/get/{symbol}/history/paginated",
    description=(
            "Get history of one pair with price "
            "and time of request paginated"
    ),
    summary="Get symbol history paginated",
    response_model=Page[CurrencyPairTime]
)
@cache(expire=3)
async def get_symbol_history_paginated_handler(symbol: SymbolsEnum, uow: UOWDep):
    users = await CurrencyPairsService().get_history_of_symbol_paginated(uow, symbol=symbol.value)
    return users
