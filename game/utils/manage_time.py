"""Засекам время, для рейтинговой таблицы."""

import time
from pathlib import Path

from game.utils import api

TIME_DUMP_FILE = Path("time.txt")


def save_time() -> None:
    """Сохраняем время начала игры."""
    with TIME_DUMP_FILE.open("w") as f:
        f.write(str(int(time.time())))


def get_start_time() -> int | None:
    """Получаем время начала игры."""
    if not TIME_DUMP_FILE.exists():
        return None
    with TIME_DUMP_FILE.open() as f:
        return int(f.read())


def get_status() -> str:
    start_time = get_start_time()

    if not start_time:
        return "Для участия в рейтинговом зачёте необходимо пройти все уровни."

    res_time = int(time.time() - start_time)
    api.pin_res(res_time)

    leaders = api.get_leaders()
    leaders_text = "\n\n" + "\n".join(
        f"{n}. {i} сек." for n, i in enumerate(leaders, start=1)
    )

    if res_time in leaders:
        return f"Ваше место в рейтинге: {leaders.index(res_time) + 1}" + leaders_text

    return "К сожалению, вам не суждено оказаться в рейтинговой таблице." + leaders_text
