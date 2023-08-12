# External import
import uuid
from dataclasses import dataclass, field
from typing import Optional


def _generate_id() -> str:
    return uuid.uuid4()


@dataclass
class ArtifactSchema:
    source_schema: dataclass
