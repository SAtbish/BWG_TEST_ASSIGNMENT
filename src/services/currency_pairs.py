from datetime import datetime
from src.schemas.currency_pairs import CurrencyPair
from src.schemas.response import CurrencyPairTime
from src.utils.unitofwork import IUnitOfWork


class CurrencyPairsService:
    @staticmethod
    async def create_currency_pair(uow: IUnitOfWork, currency_pair: CurrencyPairTime):
        async with uow:
            new_currency_pair = await uow.currency_pairs.create_one(
                data={**currency_pair.model_dump()}
            )
            await uow.commit()
            return new_currency_pair.model_dump(exclude=["id"])

    @staticmethod
    async def create_currency_pairs(uow: IUnitOfWork, currency_pairs: list[CurrencyPair]):
        request_time = datetime.now()
        async with uow:
            new_currency_pairs = await uow.currency_pairs.create_many(
                data=[
                    {**currency_pair.model_dump(), "time": request_time}
                    for currency_pair in currency_pairs
                ]
            )
            await uow.commit()
            return [
                new_currency_pair[0].to_read_model().model_dump(exclude=["id"])
                for new_currency_pair in new_currency_pairs
            ]
