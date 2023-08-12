# External imports
import unittest
from dataclasses import dataclass, fields

# Local imports
from pypipeline.schemas import BaseSchema
from pypipeline.schemas.fields import field_persistance
from pypipeline.utils._const import FIELD_PERSISTANCE

"""
Test plan:
  - test basic type setting
  - test carry, mix perishable/persitant
  - test carry, only perishable
  - test carry, only persistant
  - test generated artifact correspond with perishables
  - test generated artifact retain type from perishables
"""


class DataclassTestCase(unittest.TestCase):
    """Testcase basic datatype and values"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: str = field_persistance()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_data_content(self):
        self.assertEqual(self._dataclass.A, self._data["A"])
        self.assertEqual(self._dataclass.B, self._data["B"])

    def test_data_metadata(self):
        self.assertTrue(
            all(
                [
                    FIELD_PERSISTANCE in field.metadata
                    for field in fields(self._dataclass)
                ]
            )
        )
        self.assertTrue(
            all(
                [field.metadata[FIELD_PERSISTANCE] for field in fields(self._dataclass)]
            )
        )

    def test_data_types(self):
        self.assertTrue(all([field.type is str for field in fields(self._dataclass)]))
        self.assertTrue(
            all([isinstance(value, str) for value in self._dataclass.__dict__.values()])
        )
