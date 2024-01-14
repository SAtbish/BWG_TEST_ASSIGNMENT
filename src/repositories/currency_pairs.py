from src.models.currency_pairs import CurrencyPairModel
from src.utils.repository import SQLAlchemyRepository


class CurrencyPairRepository(SQLAlchemyRepository):
    model = CurrencyPairModel
