# External imports
from typing import TypeVar

# Local imports
from .common import IBaseStage

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type


class ITerminalStage(IBaseStage[I, O]):
    pass
