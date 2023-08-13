# External imports
import dataclasses
from dataclasses import dataclass, fields, make_dataclass
from typing import List, Set, Type

from pypipeline.schemas.fields import field_persistance
from pypipeline.utils._const import FIELD_PERSISTANCE

# Local imports
from .artifact_schema import ArtifactSchema


@dataclass
class BaseSchema:
    def _del_fields(self, fields: List[str]) -> dict:
        _temp = self.__dict__.copy()

        for field in fields:
            _temp.pop(field)

        return _temp

    def _get_fields(self, schema: dataclass) -> List[str]:
        return [v.name for v in fields(schema)]

    def _get_perishables(self, schema: dataclass) -> List[str]:
        return [v.name for v in fields(schema) if not v.metadata[FIELD_PERSISTANCE]]

    def _validate_retire(self, fields: Set[str]) -> None:
        _fields = set(self._get_fields(schema=self))
        _shared_fields = fields.intersection(_fields)

        if len(_shared_fields) != len(fields):
            _diff = set(fields) - _fields
            raise Exception(
                f"""
                  Fields to retire not present:
                    - {_diff}
                  Out of:
                    - {_fields}
                """
            )

    def _get_field_types(self, schema: dataclass) -> dict:
        return {v.name: v.type for v in fields(schema)}

    def get_artifact(self) -> ArtifactSchema:
        _perishables = self._get_perishables(schema=self)
        _base_fields = self._get_fields(schema=self)

        artifact_fields = set(_base_fields) - set(_perishables)
        _fields = [
            (n, t)
            for n, t in self._get_field_types(schema=self).items()
            if n in _perishables
        ]
        _values = self._del_fields(artifact_fields)

        return make_dataclass("Artifact", fields=_fields, bases=(ArtifactSchema,))(
            **_values, source_schema=self.__class__
        )

    def get_carry(self) -> dict:
        _perishables = self._get_perishables(schema=self)

        return self._del_fields(_perishables)
