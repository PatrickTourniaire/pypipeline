# External imports
import unittest
from dataclasses import dataclass
from typing import Tuple, get_args

# Local imports
from pypipeline.schemas import BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance
from pypipeline.stages import IForwardStage, IInitStage, ITerminalStage
from pypipeline.stages.common import IBaseStage


@dataclass
class InputTest(BaseSchema):
    A: str = field_persistance()
    B: str = field_perishable()


@dataclass
class OutputTest(BaseSchema):
    A: str = field_persistance()


class BaseStageTest(IBaseStage[InputTest, OutputTest]):
    def compute(self) -> None:
        self._output = self.input.get_carry()

    def get_output(self) -> OutputTest:
        return OutputTest(**self._output)


class TypingTestCase(unittest.TestCase):
    """Test that the generics of the stage are correct"""

    def setUp(self) -> None:
        self._stage = BaseStageTest()

    def test_input_type(self):
        self.assertEqual(get_args(self._stage.__orig_bases__[0])[0], InputTest)

    def test_output_type(self):
        self.assertEqual(get_args(self._stage.__orig_bases__[0])[1], OutputTest)


class InputDataTestCase(unittest.TestCase):
    """Test that the generics of the stage are correct"""

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = InputTest(**self._data)

        self._stage = BaseStageTest()
        self._stage.set_input(self._dataclass)

    def test_input_type(self):
        self.assertEqual(self._stage.input, self._dataclass)
        self.assertEqual(self._stage.input.A, self._data["A"])
        self.assertEqual(self._stage.input.B, self._data["B"])


@dataclass
class TerminalOutputTest(BaseSchema):
    A: str = field_persistance()


class TerminalStageTest(ITerminalStage[OutputTest, TerminalOutputTest]):
    def compute(self) -> None:
        self._output = self.input.get_carry()

    def get_output(self) -> TerminalOutputTest:
        return TerminalOutputTest(**self._output)


class ForwardStageTest(IForwardStage[OutputTest, OutputTest, TerminalStageTest]):
    def compute(self) -> None:
        self._output = self.input.get_carry()

    def get_output(self) -> Tuple[TerminalStageTest, OutputTest]:
        return TerminalStageTest, OutputTest(**self._output)


class InitStageTest(IInitStage[InputTest, OutputTest, ForwardStageTest]):
    def compute(self) -> None:
        self._output = self.input.get_carry()

    def get_output(self) -> Tuple[TerminalStageTest, OutputTest]:
        return ForwardStageTest, OutputTest(**self._output)


class DiscoverTestCase(unittest.TestCase):
    """Test that the discover method returns correct refs"""

    def setUp(self) -> None:
        self._init_stage = InitStageTest()
        self._forward_stage = ForwardStageTest()

    def test_discover(self):
        self.assertEqual(self._init_stage.discover(), ForwardStageTest)
        self.assertEqual(self._forward_stage.discover(), TerminalStageTest)


class PipelineTestCase(unittest.TestCase):
    """Test that the connection with outputs is correct"""

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = InputTest(**self._data)

        self._stage = InitStageTest()
        self._stage.set_input(self._dataclass)
        self._stage.compute()

    def test_correct_next(self):
        forward_ref, output = self._stage.get_output()
        forward_stage = forward_ref()
        forward_stage.set_input(output)
        forward_stage.compute()

        terminal_ref, _ = forward_stage.get_output()

        self.assertEqual(forward_ref, ForwardStageTest)
        self.assertEqual(terminal_ref, TerminalStageTest)

    def test_correct_data(self):
        forward_ref, init_output = self._stage.get_output()
        forward_stage = forward_ref()
        forward_stage.set_input(init_output)
        forward_stage.compute()

        terminal_ref, forward_output = forward_stage.get_output()
        terminal_stage = terminal_ref()
        terminal_stage.set_input(forward_output)
        terminal_stage.compute()
        terminal_output = terminal_stage.get_output()

        self.assertIsInstance(init_output, OutputTest)
        self.assertIsInstance(forward_output, OutputTest)
        self.assertIsInstance(terminal_output, TerminalOutputTest)
