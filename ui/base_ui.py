from entities.entity_manager import EntityManager
from utils import Utils


class BaseUI:
    def __init__(self, entity_manager: EntityManager = None):
        self.entity_manager = entity_manager
        self.utils = Utils(entity_manager)

    def main(self):
        pass
