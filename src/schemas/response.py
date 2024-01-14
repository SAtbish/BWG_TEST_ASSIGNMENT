from src.schemas.base import ResponseModel
from src.schemas.currency_pairs import CurrencyPairTime


class AllSymbolsResponse(ResponseModel):
    data: list[CurrencyPairTime]


class OneSymbolResponse(ResponseModel):
    data: CurrencyPairTime
