"""Работа с API.

Документация: https://lb.iamlostshe.ru/redoc
"""

from requests import Session

_BASE_URL = "https://lb.iamlostshe.ru/"

session = Session()

def pin_res(res_time: int) -> None:
    session.get(
        _BASE_URL + "add",
        params={"time": res_time},
        timeout=5,
    )


def get_leaders() -> list:
    return session.get(
        _BASE_URL + "res",
        timeout=5,
    ).json()
