from datetime import datetime

from fastapi import status
from .router import router
from src.schemas.response import CurrencyPairTime
from src.utils.create_response import create_response
from src.api.dependencies import UOWDep
from src.schemas.base import ResponseModel
from src.services.currency_pairs import CurrencyPairsService
from src.utils.binance_websocket import websocket_worker


@router.get(
    "/update/{symbol}",
    description=(
            "Save one pair with price "
            "and time of request to database."
    ),
    summary="Save one symbols pair",
    response_model=ResponseModel,
    responses={
        status.HTTP_201_CREATED: {
            "model": ResponseModel,
            "description": "Pair saved.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,
            "description": "Pair not saved.",
        }
    }
)
async def update_one_symbol_pare_handler(symbol: str, uow: UOWDep):
    request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    symbol_data, err = await websocket_worker.get_symbol(symbol)
    if err:
        return create_response(
            content=ResponseModel(
                message=err
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    currency_pair = CurrencyPairTime(**symbol_data, time=request_time)
    err = await CurrencyPairsService().create_currency_pair(
        uow=uow,
        currency_pair=currency_pair
    )
    if err:
        return create_response(
            content=ResponseModel(
                message=err
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    return create_response(
        content=ResponseModel(
            message="Pair received and saved"
        ),
        status=status.HTTP_201_CREATED
    )
