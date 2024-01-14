from datetime import datetime

from fastapi import status
from .router import router
from src.schemas.response import OneSymbolResponse, CurrencyPairTime
from src.schemas.request import SymbolsEnum
from src.utils.binance_client import BinanceClient
from src.utils.create_response import create_response
from src.api.dependencies import UOWDep
from src.schemas.base import ResponseModel
from src.services.currency_pairs import CurrencyPairsService


@router.get(
    "/get/{symbol}",
    description=(
            "Get one pair with price "
            "and time of request and save to database."
    ),
    summary="Get one symbols pair",
    response_model=OneSymbolResponse,
    responses={
        status.HTTP_201_CREATED: {
            "model": OneSymbolResponse,
            "description": "Pair received.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,
            "description": "Pair not received.",
        }
    }
)
async def get_one_symbol_pare_handler(symbol: SymbolsEnum, uow: UOWDep):
    bc = BinanceClient()
    request_time = datetime.now()
    async with bc:
        symbol_data, err = await bc.get_one_ticker(symbol=symbol.value)
        if err:
            return create_response(
                content=ResponseModel(
                    message=err
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        currency_pair = CurrencyPairTime(**symbol_data, time=request_time)
        currency_pair_data = await CurrencyPairsService().create_currency_pair(
            uow=uow,
            currency_pair=currency_pair
        )
    return create_response(
        content=OneSymbolResponse(
            data=currency_pair_data,
            message="Pair received and saved"
        ),
        status=status.HTTP_201_CREATED
    )
