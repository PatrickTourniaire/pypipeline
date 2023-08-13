# Local imports
# External import
from dataclasses import Field, field

from pypipeline.utils._const import FIELD_PERSISTANCE


def field_persistance(**kwargs) -> Field:
    return field(metadata={FIELD_PERSISTANCE: True}, **kwargs)
