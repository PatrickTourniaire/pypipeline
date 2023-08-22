# External imports
import unittest
from dataclasses import dataclass

# Local imports
from pypipeline.schemas import ArtifactSchema, BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance


class SourceSchemaTestCase(unittest.TestCase):
    """Test case to make sure source_schema is set correctly"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_perishable()
        B: str = field_perishable()
        C: str = field_persistance()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B", "C": "C"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_source_schema(self):
        artifact = self._dataclass.get_artifact()

        self.assertEqual(artifact.source_schema, self.TestDataclass)


class BasicFieldsTestCase(unittest.TestCase):
    """Test case to ensure that fields can be set properly"""

    @dataclass
    class TestDataclass(ArtifactSchema):
        A: str
        B: dict
        C: list

    def setUp(self) -> None:
        self._data = {"A": "A", "B": {}, "C": []}
        self._dataclass = self.TestDataclass(source_schema=None, **self._data)

    def test_field_values(self):
        self.assertEqual(self._dataclass.A, self._data["A"])
        self.assertEqual(self._dataclass.B, self._data["B"])
        self.assertEqual(self._dataclass.C, self._data["C"])

    def test_field_types(self):
        self.assertIsInstance(self._dataclass.A, str)
        self.assertIsInstance(self._dataclass.B, dict)
        self.assertIsInstance(self._dataclass.C, list)
