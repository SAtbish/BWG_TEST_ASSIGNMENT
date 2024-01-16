import aiohttp

get_symbols_price = {
    "id": "BWG_TEST",
    "method": "ticker.price"
}


class WebsocketWorker:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.connection = self.session.ws_connect("wss://ws-api.binance.com:9443/ws-api/v3")

    async def initialize_session(self):
        self.session = aiohttp.ClientSession()
        self.connection = await self.session.ws_connect("wss://ws-api.binance.com:9443/ws-api/v3")

    @staticmethod
    def validate_response(data: dict):
        if "result" in data:
            return data["result"], None
        else:
            return None, data.get('error', {}).get("msg", "error")

    async def get_symbol(self, symbol: str):
        try:
            await self.connection.send_json(
                {
                    **get_symbols_price,
                    "params": {
                        "symbol": symbol
                    }
                }
            )
            data = await self.connection.receive_json()
            response = WebsocketWorker.validate_response(data)
            return response
        except Exception as e:
            return {}, str(e)

    async def get_symbols(self):
        try:
            await self.connection.send_json(get_symbols_price)
            data = await self.connection.receive_json()
            response = WebsocketWorker.validate_response(data)
            return response
        except Exception as e:
            return {}, str(e)

    def __del__(self):
        self.connection.close()
        self.session.close()


websocket_worker = WebsocketWorker()
