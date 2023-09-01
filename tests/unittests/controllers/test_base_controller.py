# External imports
import unittest
from dataclasses import dataclass
from typing import Tuple

# Local imports
from pypipeline.schemas import BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance
from pypipeline.stages import IForwardStage, IInitStage, ITerminalStage
from pypipeline.controlers.common import BaseController


"""=============================== TEST DATA =============================="""


@dataclass
class InputTest(BaseSchema):
    A: str = field_persistance()
    B: str = field_perishable()


@dataclass
class OutputTest(BaseSchema):
    A: str = field_perishable()
    C: str = field_persistance()


@dataclass
class TerminalOutputTest(BaseSchema):
    C: str = field_persistance()


class TerminalStageTest(ITerminalStage[OutputTest, TerminalOutputTest]):

    def compute(self) -> None:
        self._output = self.input.get_carry()

    def get_output(self) -> TerminalOutputTest:
        return TerminalOutputTest(**self._output)


class ForwardStageTest(
    IForwardStage[OutputTest, OutputTest, TerminalStageTest]
):

    def compute(self) -> None:
        self._output = self.input.__dict__

    def get_output(self) -> Tuple[TerminalStageTest, OutputTest]:
        return TerminalStageTest(), OutputTest(**self._output)


class InitStageTest(IInitStage[InputTest, OutputTest, ForwardStageTest]):

    def compute(self) -> None:
        self._output = {**self.input.get_carry(), 'C': 'C'}

    def get_output(self) -> Tuple[ForwardStageTest, OutputTest]:
        return ForwardStageTest(), OutputTest(**self._output)


"""============================== TEST CASES =============================="""


class ForwardPassTestCase(unittest.TestCase):
    """Test that the forward pass is successfull"""

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = InputTest(**self._data)
        self._stage = InitStageTest

        self._controller = BaseController(self._dataclass, self._stage)

    def test_forward_pass(self):
        output, run_id = self._controller.start()

        self.assertIsInstance(output, TerminalOutputTest)
        self.assertEqual(output.C, 'C')
        self.assertIsInstance(run_id, str)


class CheckArtifactsTestCase(unittest.TestCase):
    """Test that all artifacts are present with correct values"""

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = InputTest(**self._data)
        self._stage = InitStageTest

        self._controller = BaseController(self._dataclass, self._stage)

    def test_artifacts(self):
        _, run_id = self._controller.start()
        artifacts = self._controller.get_artifacts(run_id)

        self.assertIs(artifacts['InitStageTest'].source_schema, InputTest)
        self.assertSetEqual(
            set(
                artifacts['InitStageTest'].__dict__.keys()
            ) - set(['source_schema']),
            set(['B'])
        )

        self.assertIs(artifacts['ForwardStageTest'].source_schema, OutputTest)
        self.assertSetEqual(
            set(
                artifacts['ForwardStageTest'].__dict__.keys()
            ) - set(['source_schema']),
            set(['A'])
        )

        self.assertIs(
            artifacts['TerminalStageTest'].source_schema,
            TerminalOutputTest
        )
        self.assertSetEqual(
            set(
                artifacts['TerminalStageTest'].__dict__.keys()
            ) - set(['source_schema']),
            set()
        )
