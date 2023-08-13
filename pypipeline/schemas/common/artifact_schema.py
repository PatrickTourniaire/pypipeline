# External import
from dataclasses import dataclass


@dataclass
class ArtifactSchema:
    source_schema: dataclass

    def get_standard_fields(self):
        return ["source_schema"]
