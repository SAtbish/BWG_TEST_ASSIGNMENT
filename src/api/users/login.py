from src.api.users.router import router
from fastapi import status

from src.schemas.base import ResponseModel
from src.schemas.users import UserLogin
from src.utils.create_response import create_response


@router.post(
    "/login",
    response_model=ResponseModel,
    status_code=status.HTTP_200_OK,
    description=(
            "User Authorization"
    ),
    summary="Authorize user",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseModel,
            "description": "User authorized",
        },
        status.HTTP_409_CONFLICT: {
            "model": ResponseModel,
            "description": "User not authorized. Check message",
        }
    }
)
async def user_login_handler(
        user: UserLogin
):
    if user.password != 12345678 and user.login != "A":
        response = create_response(
            content=ResponseModel(message="not correct login or password"),
            status=status.HTTP_409_CONFLICT
        )
    else:
        response = create_response(
            content=ResponseModel(
                message="User log in"
            ),
            status=status.HTTP_200_OK
        )
        response.set_cookie("access_token", "token", samesite="none", secure=True)

    return response
