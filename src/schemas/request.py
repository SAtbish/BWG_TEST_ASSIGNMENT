from enum import Enum
import asyncio
from src.utils.binance_client import BinanceClient
import nest_asyncio
nest_asyncio.apply()


async def get_all_symbols():
    bc = BinanceClient()
    async with bc:
        return await bc.get_all_symbols()

symbols = asyncio.run(get_all_symbols())
SymbolsEnum = Enum("SymbolsEnum", symbols)
