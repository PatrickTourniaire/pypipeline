# Local imports
# External import
from dataclasses import Field, field

from pypipeline.stages.common import IBaseStage
from pypipeline.utils._const import FIELD_PERSISTANCE


def field_perishable(**kwargs) -> Field:
    return field(metadata={FIELD_PERSISTANCE: False}, **kwargs)
