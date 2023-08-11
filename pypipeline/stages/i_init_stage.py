# External imports
from typing import Generic, Tuple, TypeVar, get_args

# Local imports
from .common import IBaseStage

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type
N = TypeVar("N", bound=IBaseStage)  # Next stage reference


class IInitStage(IBaseStage[I, O], Generic[I, O, N]):
    def __init_subclass__(cls) -> None:
        cls._types = get_args(cls.__orig_bases__[0])

    # ---------------------------------------------------------------------------
    #                            PUBLIC METHODS
    # ---------------------------------------------------------------------------
    def discover(self) -> N:
        return self._types[-1]

    def get_output(self) -> Tuple[N, O]:
        pass
