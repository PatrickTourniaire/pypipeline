# External import
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ArtifactSchema:
    source_schema: dataclass

    def get_standard_fields(self):
        return ["source_schema"]
