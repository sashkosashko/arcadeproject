"""Звуки используемые в игре."""

from pathlib import Path

from arcade import load_sound

YES_I_HAD_TO_GO_TO_EXTREME_MEASURES = load_sound(
    Path("assets") / "sounds" / "да_мне_пришлось_пойти_на_крайние_меры.mp3",
)
WHY = load_sound(Path("assets") / "sounds" / "зачем.mp3")
WELL_DONE = load_sound(Path("assets") / "sounds" / "маладец.mp3")
BEGINNING = load_sound(Path("assets") / "sounds" / "начало.mp3")
HELLO_ITS_ME_REMEMBER_ME = load_sound(
    Path("assets") / "sounds" / "привет_это_я_помнишь_меня.mp3",
)
BLUE_CROSSES = load_sound(Path("assets") / "sounds" / "сини_крыжочки.mp3")
HOORAY = load_sound(Path("assets") / "sounds" / "ура.mp3")
PHEW_WE_DID_IT = load_sound(Path("assets") / "sounds" / "фух_мы_справились.mp3")
I_WOULDNT_GO_THERE = load_sound(Path("assets") / "sounds" / "я_бы_туда_не_ходила.mp3")
