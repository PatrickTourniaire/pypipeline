# External imports
from typing import TypeVar, get_args

# Local imports
from .common import IBaseStage

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type


class ITerminalStage(IBaseStage[I, O]):
    def __init_subclass__(cls) -> None:
        cls._types = get_args(cls.__orig_bases__[0])

    def discover(self) -> None:
        return None

    def input_schema(self) -> I:
        return self._types[0]

    def output_schema(self) -> O:
        return self._types[-1]
