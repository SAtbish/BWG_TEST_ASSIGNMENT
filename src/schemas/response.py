from src.schemas.base import ResponseModel
from src.schemas.currency_pairs import CurrencyPairTime
from pydantic import BaseModel, Field


class AddedRows(BaseModel):
    count: int = Field(gt=0)


class AddedRowsResponse(ResponseModel):
    data: AddedRows


class AllSymbolsResponse(ResponseModel):
    data: list[CurrencyPairTime]


class OneSymbolResponse(ResponseModel):
    data: CurrencyPairTime
