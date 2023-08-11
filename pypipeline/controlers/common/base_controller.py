# Local imports
from stages import BaseStage


class BaseController:
    def __init__(self, path: list):
        self.path = path

    def data_init(self, data: any):
        pass
