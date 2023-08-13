# External imports
from typing import Generic, TypeVar, get_args

# Generics
I = TypeVar("I")  # Input data type
O = TypeVar("O")  # Output data type


class IBaseStage(Generic[I, O]):
    def __str__(self) -> str:
        return f"hello"

    def __repr__(self):
        pass

    def set_input(self, input: I) -> None:
        self.input = input

    def compute(self) -> None:
        pass

    def get_output(self) -> O:
        pass
