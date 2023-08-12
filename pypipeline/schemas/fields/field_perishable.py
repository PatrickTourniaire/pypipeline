# Local imports
# External import
from dataclasses import field

from pypipeline.stages.common import IBaseStage
from pypipeline.utils._const import FIELD_PERSISTANCE


def field_perishable(**kwargs) -> field:
    return field(metadata={FIELD_PERSISTANCE: False}, **kwargs)
