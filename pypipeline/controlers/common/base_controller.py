# External imports
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
