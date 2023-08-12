# Local imports
# External import
from dataclasses import field

from pypipeline.utils._const import FIELD_PERSISTANCE


def field_persistance(**kwargs) -> field:
    return field(metadata={FIELD_PERSISTANCE: True}, **kwargs)
