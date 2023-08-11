# External imports
from dataclasses import dataclass

# Local imports
from pypipeline.stages import IForwardStage, IInitStage, ITerminalStage


@dataclass
class InitInput:
    test: str


@dataclass
class InitOutput(InitInput):
    pass


@dataclass
class ForwardInput(InitOutput):
    pass


@dataclass
class ForwardOutput(ForwardInput):
    pass


@dataclass
class TerminalInput(ForwardOutput):
    pass


@dataclass
class TerminalOutput(TerminalInput):
    pass


class TerminalStage(ITerminalStage[TerminalInput, TerminalOutput]):
    def compute(self) -> None:
        self.test = self.input.test

    def get_output(self) -> TerminalOutput:
        return TerminalOutput(**self.input.__dict__)


class ForwardStage(IForwardStage[ForwardInput, ForwardOutput, TerminalStage]):
    def compute(self) -> None:
        self.test = self.input.test


class InitStage(IInitStage[InitInput, InitOutput, ForwardStage]):
    def compute(self) -> None:
        self.test = self.input.test


A = InitStage()

B = A.discover()
B = B()
print(f"B - {B}")

C = B.discover()
print(f"C - {C()}")
