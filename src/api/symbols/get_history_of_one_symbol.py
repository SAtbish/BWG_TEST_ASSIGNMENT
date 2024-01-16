from fastapi import status
from .router import router
from src.schemas.response import AllSymbolsResponse
from src.schemas.request import SymbolsEnum
from src.utils.create_response import create_response
from src.api.dependencies import UOWDep
from src.schemas.base import ResponseModel
from src.services.currency_pairs import CurrencyPairsService
from fastapi_cache.decorator import cache


@router.get(
    "/get/{symbol}/history",
    description=(
            "Get history of one pair with price "
            "and time of request"
    ),
    summary="Get symbol history",
    response_model=AllSymbolsResponse,
    responses={
        status.HTTP_200_OK: {
            "model": AllSymbolsResponse,
            "description": "Pair received.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,
            "description": "Pair not received.",
        }
    }
)
@cache(expire=3)
async def get_symbol_history_handler(symbol: SymbolsEnum, uow: UOWDep):
    data, err = await CurrencyPairsService().get_history_of_symbol(
        uow=uow,
        symbol=symbol.value
    )
    if err:
        return create_response(
            content=ResponseModel(
                message=err
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    return create_response(
        content=AllSymbolsResponse(
            data=data,
            message="Pair received and saved"
        ),
        status=status.HTTP_200_OK
    )
