from fastapi import status
from .router import router
from src.schemas.response import OneSymbolResponse
from src.utils.create_response import create_response
from src.api.dependencies import UOWDep
from src.schemas.base import ResponseModel
from src.services.currency_pairs import CurrencyPairsService
from fastapi_cache.decorator import cache


@router.get(
    "/get/{symbol}/last",
    description=(
            "Get one pair with price "
            "and time of request from database"
    ),
    summary="Get last one symbols pair from database",
    response_model=OneSymbolResponse,
    responses={
        status.HTTP_200_OK: {
            "model": OneSymbolResponse,
            "description": "Pair received.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,
            "description": "Pair not received.",
        }
    }
)
@cache(expire=3)
async def get_symbol_history_handler(symbol: str, uow: UOWDep):
    data, err = await CurrencyPairsService().get_last_data_of_symbol(
        uow=uow,
        symbol=symbol
    )
    if err:
        return create_response(
            content=ResponseModel(
                message=err
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    return create_response(
        content=OneSymbolResponse(
            data=data,
            message="Pair received"
        ),
        status=status.HTTP_200_OK
    )
