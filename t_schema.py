from dataclasses import dataclass

from pypipeline.schemas import BaseSchema
from pypipeline.schemas.fields import field_perishable, field_persistance


@dataclass
class TestInput(BaseSchema):
    testA: str = field_persistance()
    testB: str = field_perishable()
    testC: str = field_persistance()


@dataclass
class TestOutput(BaseSchema):
    testA: str = field_persistance()
    testC: str = field_perishable()
    testY: str = field_perishable()


@dataclass
class TestTerminalOutput(BaseSchema):
    testA: str = field_persistance()
    testD: str = field_persistance()
