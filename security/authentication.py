import secrets
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from decouple import config

security = HTTPBasic()


def authenticate_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> None:
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = str.encode(config("API_USER"))
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = str.encode(config("API_PASSWORD"))
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return
