from dataclasses import dataclass, fields
from typing import Tuple

from pypipeline.schemas import ArtifactSchema, BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance
from pypipeline.stages import IInitStage, ITerminalStage
from t_schema import TestInput, TestOutput, TestTerminalOutput


class TerminalStage(ITerminalStage[TestOutput, TestTerminalOutput]):
    def compute(self) -> None:
        self.test = ""

    def get_output(self) -> TestTerminalOutput:
        _carry = self.input.get_carry()
        return TestTerminalOutput(**_carry, testD="testD")


class InitStage(IInitStage[TestInput, TestOutput, TerminalStage]):
    def compute(self) -> None:
        self.test = ""

    def get_output(self) -> Tuple[TerminalStage, TestOutput]:
        _carry = self.input.get_carry()
        return TerminalStage(), TestOutput(**_carry, testY="testY")


test = TestInput(testA="testA", testB="testB", testC="testC")

stageA = InitStage()
stageA.set_input(test)
stageA.compute()
stageB, stageAOutput = stageA.get_output()

print()
print(stageAOutput)
print()

stageB.set_input(stageAOutput)
stageB.compute()
stageBOutput = stageB.get_output()

print()
print(stageBOutput)
print()
