# External imports
import unittest
from dataclasses import dataclass, fields

# Local imports
from pypipeline.schemas import ArtifactSchema, BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance
from pypipeline.utils._const import FIELD_PERSISTANCE


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


class MixFieldsTestCase(unittest.TestCase):
    """Testcase with mixed perishable and persistant fields"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: str = field_perishable()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_data_perishable(self):
        self.assertEqual(self._dataclass.B, self._data["B"])

    def test_metadata_perishable(self):
        self.assertTrue(FIELD_PERSISTANCE in fields(self._dataclass)[1].metadata)
        self.assertFalse(fields(self._dataclass)[1].metadata[FIELD_PERSISTANCE])

    def test_carry(self):
        _carry = self._dataclass.get_carry()

        self.assertIsInstance(_carry, dict)
        self.assertTrue(set(["A"]) == set(_carry.keys()))
        self.assertTrue(
            all(
                [
                    field.type is str
                    for field in fields(self._dataclass)
                    if field.name == "A"
                ]
            )
        )

    def test_artifact(self):
        _artifact = self._dataclass.get_artifact()
        standard_fields = set(_artifact.get_standard_fields())
        custom_fields = set(_artifact.__dict__.keys()) - standard_fields

        self.assertIsInstance(_artifact, ArtifactSchema)
        self.assertTrue(set(["B"]) == custom_fields)
        self.assertTrue(
            all(
                [
                    field.type is str
                    for field in fields(self._dataclass)
                    if field.name == "B"
                ]
            )
        )


class OnlyPerishablesTestCase(unittest.TestCase):
    """Testcase with only perishable fields"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_perishable()
        B: str = field_perishable()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_data_perishable(self):
        self.assertEqual(self._dataclass.B, self._data["B"])
        self.assertEqual(self._dataclass.A, self._data["A"])

    def test_metadata_perishable(self):
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
                [
                    not field.metadata[FIELD_PERSISTANCE]
                    for field in fields(self._dataclass)
                ]
            )
        )

    def test_carry(self):
        _carry = self._dataclass.get_carry()

        self.assertIsInstance(_carry, dict)
        self.assertTrue(len(_carry.keys()) == 0)
        self.assertEqual(_carry, {})

    def test_artifact(self):
        _artifact = self._dataclass.get_artifact()
        standard_fields = set(_artifact.get_standard_fields())
        custom_fields = set(_artifact.__dict__.keys()) - standard_fields

        self.assertIsInstance(_artifact, ArtifactSchema)
        self.assertTrue(set(["A", "B"]) == custom_fields)
        self.assertTrue(
            all(
                [
                    field.type is str
                    for field in fields(self._dataclass)
                    if field.name in ["A", "B"]
                ]
            )
        )


class OnlyPersistantsTestCase(unittest.TestCase):
    """Testcase for base schema with only persistant fields"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: str = field_persistance()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_data_persistant(self):
        self.assertEqual(self._dataclass.A, self._data["A"])
        self.assertEqual(self._dataclass.B, self._data["B"])

    def test_metadata_persistance(self):
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

    def test_carry(self):
        _carry = self._dataclass.get_carry()

        self.assertIsInstance(_carry, dict)
        self.assertTrue(set(["A", "B"]) == set(_carry.keys()))
        self.assertTrue(
            all([self._data[name] == value for name, value in _carry.items()])
        )

    def test_artifact(self):
        _artifact = self._dataclass.get_artifact()
        standard_fields = set(_artifact.get_standard_fields())
        custom_fields = set(_artifact.__dict__.keys()) - standard_fields

        self.assertIsInstance(_artifact, ArtifactSchema)
        self.assertTrue(len(custom_fields) == 0)


class PrivateGetFieldsTestCase(unittest.TestCase):
    """Testcase for private get fields method"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: str = field_persistance()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_fields(self):
        self.assertSetEqual(
            set(self._dataclass._get_fields(self._dataclass)), set(self._data.keys())
        )


class PrivateGetPerishablesTestCase(unittest.TestCase):
    """Testcase for private get perishables method"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: str = field_perishable()
        C: str = field_perishable()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B", "C": "C"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_fields_perishables(self):
        self.assertSetEqual(
            set(self._dataclass._get_perishables(self._dataclass)), set(["B", "C"])
        )


class PrivateGetFieldTypesTestCase(unittest.TestCase):
    """Testcase for private get field types method"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: dict = field_persistance()
        C: int = field_persistance()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B", "C": "C"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_field_types(self):
        _types = self._dataclass._get_field_types(self._dataclass)

        self.assertEqual(_types["A"], str)
        self.assertEqual(_types["B"], dict)
        self.assertEqual(_types["C"], int)


class PrivateDelFieldsTestCase(unittest.TestCase):
    """Testcase for private del fields dict generated"""

    @dataclass
    class TestDataclass(BaseSchema):
        A: str = field_persistance()
        B: dict = field_persistance()
        C: int = field_persistance()

    def setUp(self) -> None:
        self._data = {"A": "A", "B": "B", "C": "C"}
        self._dataclass = self.TestDataclass(**self._data)

    def test_del_fields(self):
        _del_fields = ["A", "C"]
        _remainder = self._dataclass._del_fields(_del_fields)

        self.assertTrue(len(set(_del_fields).intersection(set(_remainder))) == 0)
        self.assertSetEqual(set(_remainder.keys()), set(["B"]))
        self.assertEqual(_remainder["B"], self._data["B"])
