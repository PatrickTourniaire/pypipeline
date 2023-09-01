# External imports
import uuid
from collections import defaultdict
from typing import Tuple

from rich.console import Console
from rich.table import Table

# Local imports
from pypipeline.schemas import BaseSchema
from pypipeline.stages import IInitStage, ITerminalStage
from pypipeline.stages.common import IBaseStage


class BaseController:
    def __init__(self, init_data: BaseSchema, init_stage: IInitStage):
        self.init_data = init_data
        self.init_stage = init_stage

        self._artifact_cache = defaultdict(dict)

    def _generate_discover_table(self) -> Table:
        table = Table(title="Discover")

        table.add_column("Stage No.", style="cyan", no_wrap=True)
        table.add_column("Stage Name", justify="center", style="magenta")
        table.add_column("Input Data", justify="center", style="green")
        table.add_column("Output Data", justify="center", style="red")
        table.add_column("Next Stage", justify="right", style="green")

        return table

    def _stage_name(self, stage: IBaseStage) -> str:
        return stage.__class__.__name__

    def discover(self) -> None:
        table = self._generate_discover_table()
        stage = self.init_stage()
        stage_no = 0

        table.add_row(
            str(stage_no),
            self._stage_name(stage),
            str(stage.input_schema()),
            str(stage.output_schema()),
            str(stage.discover()),
        )

        while not isinstance(stage, ITerminalStage):
            stage = stage.discover()
            stage = stage()
            stage_no += 1

            table.add_row(
                str(stage_no),
                self._stage_name(stage),
                str(stage.input_schema()),
                str(stage.output_schema()),
                str(stage.discover()),
            )

        console = Console()
        console.print(table)

    def start(self) -> Tuple[BaseSchema, str]:
        run_id = str(uuid.uuid4())

        stage = self.init_stage()
        stage.set_input(self.init_data)

        while not isinstance(stage, ITerminalStage):
            # Cache artifact
            self._artifact_cache[run_id][
                stage.__class__.__name__
            ] = stage.input.get_artifact()

            # Compute and get next output
            stage.compute()
            stage, output = stage.get_output()

            if isinstance(stage, type):
                raise ReferenceError(
                    "The get_object method needs to return an instance!",
                    stage
                )

            stage.set_input(output)

        # Get terminal output and artifact
        stage.compute()
        output = stage.get_output()
        self._artifact_cache[run_id][
            stage.__class__.__name__
        ] = stage.input.get_artifact()
        self._artifact_cache[run_id][stage.__class__.__name__] = output.get_artifact()

        return output, run_id

    def get_artifacts(self, run_id: str) -> dict:
        return self._artifact_cache[run_id]
