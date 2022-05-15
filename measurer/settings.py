from dataclasses import dataclass
from typing import Final

ICON_PATH: Final = "../assets/icons"


@dataclass(frozen=True, slots=True)
class RotateDirection:
    __cw: int = 90
    __ccw: int = -90

    @property
    def cw(self) -> int:
        return self.__cw

    @property
    def ccw(self) -> int:
        return self.__ccw


@dataclass(frozen=True, slots=True)
class AxisDirection:
    __horizontal: tuple[float, float] = (-1, 1)
    __vertical: tuple[float, float] = (1, -1)

    @property
    def horizontal(self) -> tuple[float, float]:
        return self.__horizontal

    @property
    def vertical(self) -> tuple[float, float]:
        return self.__vertical
