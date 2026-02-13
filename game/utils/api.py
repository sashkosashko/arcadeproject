"""Работа с API.

Документация: http://lb.iamlostshe.ru:8000/redoc
"""

from requests import Session

_BASE_URL = "http://lb.iamlostshe.ru:8000/"

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
