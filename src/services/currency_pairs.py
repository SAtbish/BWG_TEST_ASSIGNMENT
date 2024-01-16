from datetime import datetime
from src.schemas.currency_pairs import CurrencyPair
from src.schemas.response import CurrencyPairTime
from src.utils.unitofwork import IUnitOfWork


class CurrencyPairsService:
    @staticmethod
    async def create_currency_pair(uow: IUnitOfWork, currency_pair: CurrencyPairTime):
        async with uow:
            try:
                await uow.currency_pairs.create_one(
                    data={**currency_pair.model_dump()}
                )
                await uow.commit()
            except Exception as e:
                return str(e)

    @staticmethod
    async def create_currency_pairs(uow: IUnitOfWork, currency_pairs: list[CurrencyPair]):
        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        async with uow:
            try:
                await uow.currency_pairs.create_many(
                    data=[
                        {**currency_pair.model_dump(), "time": request_time}
                        for currency_pair in currency_pairs
                    ]
                )
                await uow.commit()
            except Exception as e:
                return str(e)

    @staticmethod
    async def get_history_of_symbol(uow: IUnitOfWork, symbol: str):
        async with uow:
            try:
                data, err = await uow.currency_pairs.get_all(symbol=symbol)
                if err:
                    return None, err
                return data, None
            except Exception as e:
                return {}, str(e)

    @staticmethod
    async def get_history_of_symbol_paginated(uow: IUnitOfWork, symbol: str):
        async with uow:
            try:
                data = await uow.currency_pairs.get_all_paginated(symbol=symbol)
                return data
            except Exception as e:
                return str(e)

    @staticmethod
    async def get_last_data_of_symbol(uow: IUnitOfWork, symbol: str):
        async with uow:
            try:
                data, err = await uow.currency_pairs.read_last(symbol=symbol)
                if err:
                    return None, err
                return data, None
            except Exception as e:
                return {}, str(e)
