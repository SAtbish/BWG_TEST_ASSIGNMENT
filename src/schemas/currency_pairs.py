from pydantic import BaseModel, Field, constr
from datetime import datetime


class CurrencyPair(BaseModel):
    symbol: str = constr(pattern="[A-Z]")
    price: float = Field(gt=0)


class CurrencyPairTime(CurrencyPair):
    time: str


class AllSymbols(BaseModel):
    symbols: list[CurrencyPair]
    time: datetime


class CurrencyPairTimeModel(CurrencyPairTime):
    id: int
