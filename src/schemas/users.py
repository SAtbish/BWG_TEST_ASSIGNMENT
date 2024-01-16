from pydantic import BaseModel, Field, constr


class UserLogin(BaseModel):
    login: str = Field(min_length=1, max_length=64, description="User login")
    password: constr(pattern="^[A-Za-z0-9-!№;$%^&*():?/|.,~`]+$", min_length=8, max_length=64)
