# External imports
import unittest
from dataclasses import Field

# Local imports
from ror.schemas.fields import field_persistance
from ror.utils._const import FIELD_PERSISTANCE


class MetaDataTestCase(unittest.TestCase):
    """Testcase for checking that the metadata field is set"""

    def setUp(self) -> None:
        self._field = field_persistance()

    def test_field_metadata(self):
        self.assertIsInstance(self._field, Field)
        self.assertTrue(FIELD_PERSISTANCE in self._field.metadata)
        self.assertTrue(self._field.metadata[FIELD_PERSISTANCE])


class KwargsTestCase(unittest.TestCase):
    """Testcase for checking that other attributes are passed to Field"""

    def setUp(self) -> None:
        self._field = field_persistance(default="_field")

    def test_kwargs(self):
        self.assertIsInstance(self._field, Field)
        self.assertEqual(self._field.default, "_field")
