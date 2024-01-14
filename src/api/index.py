from datetime import datetime

from main import app
from fastapi.responses import JSONResponse
from fastapi import status
from src.schemas.base import ResponseModel
from src.utils.binance_client import BinanceClient
from src.utils.create_response import create_response

route_description = {
    'response_model': ResponseModel,
    'status_code': status.HTTP_200_OK,
    'tags': ["index"],
    'description': (
        "Check availability of application and BinanceApi"
    ),
    'summary': "Check app",
    "responses": {
        status.HTTP_200_OK: {
            "model": ResponseModel,
            "description": "Server working",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ResponseModel,
            "description": "Server not working",
        }
    }
}


@app.get("/", **route_description)
@app.get("/ping", **route_description)
async def index_handler():
    bc = BinanceClient()
    async with bc:
        _, err = await bc.ping()
        if err:
            return create_response(
                content=ResponseModel(message=err),
                status=status.HTTP_400_BAD_REQUEST
            )
        return create_response(
            content=ResponseModel(message=f"{datetime.now()}: Working..."),
            status=status.HTTP_200_OK
        )
