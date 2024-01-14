import time

from fastapi import status
from .router import router
from src.utils.create_response import create_response
from src.utils.binance_client import BinanceClient
from src.schemas.response import AllSymbolsResponse
from src.schemas.currency_pairs import CurrencyPair
from src.api.dependencies import UOWDep
from src.schemas.base import ResponseModel
from src.services.currency_pairs import CurrencyPairsService
import logging


@router.get(
    "/get/all",
    status_code=status.HTTP_201_CREATED,
    description=(
            "Get all pairs with prices and"
            "time of request and save to database."
    ),
    summary="Get all symbols pairs",
    response_model=AllSymbolsResponse,
    responses={
        status.HTTP_201_CREATED: {
            "model": AllSymbolsResponse,
            "description": "Pairs received.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,
            "description": "Pairs not received.",
        }
    }
)
async def get_all_symbols_pairs_handler(uow: UOWDep):
    bc = BinanceClient()
    start_time = time.time()

    async with bc:
        all_tickers, err = await bc.get_all_tickers()
        get_data_time = time.time() - start_time
        if err:
            return create_response(
                content=ResponseModel(
                    message=err
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        currency_pairs = [CurrencyPair(**row) for row in all_tickers]
        currency_pairs_data = await CurrencyPairsService().create_currency_pairs(
            uow,
            currency_pairs=currency_pairs
        )

    rows_added_time = time.time() - get_data_time - start_time

    logging.warning(
        f"\nTime of getting data from Binance API: {get_data_time} seconds\n"
        f"Count of currency pairs: {len(currency_pairs_data)}\n"
        f"Time of adding data to database: {rows_added_time} seconds\n"
    )

    return create_response(
        content=AllSymbolsResponse(
            data=currency_pairs_data,
            message="All pairs received and saved"
        ),
        status=status.HTTP_201_CREATED
    )
