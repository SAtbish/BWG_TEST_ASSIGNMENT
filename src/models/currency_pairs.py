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

    def to_read_model(self) -> CurrencyPairTimeModel:
        return CurrencyPairTimeModel(
            id=self.id,
            symbol=self.symbol,
            price=self.price,
            time=self.time
        )
