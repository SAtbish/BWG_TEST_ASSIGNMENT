from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from src.db.db import Base
from src.schemas.currency_pairs import CurrencyPairTimeModel


class CurrencyPairModel(Base):
    __tablename__ = "currency_pairs"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(nullable=False)

    @classmethod
    def to_read_model(cls, *args):
        return CurrencyPairTimeModel(
            id=args[0],
            symbol=args[1],
            price=args[2],
            time=args[3].strftime('%Y-%m-%d %H:%M:%S.%f')
        )

