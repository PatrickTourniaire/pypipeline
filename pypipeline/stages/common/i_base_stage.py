# External imports
from typing import Generic, TypeVar

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type


class IBaseStage(Generic[I, O]):
    # ---------------------------------------------------------------------------
    #                           PRIVATE METHODS
    # ---------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"hello"

    def __repr__(self):
        pass

    # ---------------------------------------------------------------------------
    #                            PUBLIC METHODS
    # ---------------------------------------------------------------------------
    def set_input(self, input: I) -> None:
        self.input = input

    def compute(self) -> None:
        pass

    def get_output(self) -> O:
        pass
