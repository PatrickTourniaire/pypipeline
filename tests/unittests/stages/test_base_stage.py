# External imports
import unittest
from dataclasses import dataclass

# Local imports
from pypipeline.schemas import BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance
from pypipeline.stages.common import IBaseStage


@dataclass
class InputTest(BaseSchema):
    A: str = field_persistance()
    B: str = field_perishable()


@dataclass
class OutputTest(BaseSchema):
    A: str = field_persistance()


class StageTest(IBaseStage[InputTest, OutputTest]):
    def compute(self) -> None:
        self._output = self.input.get_carry()

    def get_output(self) -> OutputTest:
        return OutputTest(**self._output)


class InputDataTestCase(unittest.TestCase):
    """Test case for testing the process of setting an input"""

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = InputTest(**self._data)

        self._stage = StageTest()
        self._stage.set_input(self._dataclass)

    def test_input_data_value(self):
        self.assertIsInstance(self._stage.input, InputTest)
        self.assertEqual(self._stage.input.A, self._data["A"])
        self.assertEqual(self._stage.input.B, self._data["B"])


class OutputDataTestCase(unittest.TestCase):
    """Test case for testing the process of getting the output"""

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = InputTest(**self._data)

        self._stage = StageTest()
        self._stage.set_input(self._dataclass)
        self._stage.compute()

    def test_input_data_value(self):
        self.assertEqual(self._stage._output["A"], self._data["A"])
        self.assertIsInstance(self._stage.get_output(), OutputTest)
        self.assertEqual(self._stage.get_output().A, self._data["A"])
