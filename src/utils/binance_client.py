from binance import AsyncClient
from binance.exceptions import BinanceAPIException
from config import BINANCE_API_KEY, BINANCE_API_SECRET


class BinanceClient:
    def __init__(self):
        self.__api_key = BINANCE_API_KEY
        self.__api_secret = BINANCE_API_SECRET

    async def __aenter__(self):
        self.client = await AsyncClient.create(api_key=self.__api_key, api_secret=self.__api_secret)

    async def __aexit__(self, *args):
        await self.client.close_connection()

    async def get_all_tickers(self) -> tuple[dict, None | str]:
        try:
            return await self.client.get_all_tickers(), None
        except BinanceAPIException as e:
            return {}, str(e)

    async def get_all_symbols(self) -> dict[str, str]:
        data = await self.client.get_exchange_info()
        symbols = {symbol["symbol"]: symbol["symbol"] for symbol in data["symbols"]}
        return symbols

    async def get_one_ticker(self, symbol: str) -> tuple[dict, None | str]:
        try:
            return await self.client.get_symbol_ticker(symbol=symbol), None
        except BinanceAPIException as e:
            return {}, str(e)

    async def ping(self):
        try:
            return await self.client.ping(), None
        except Exception as e:
            return {}, str(e)
