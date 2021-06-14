from abc import ABC, abstractmethod
import time


class TargetList_Interface(ABC):
    __abstract__ = True

    @abstractmethod
    def parsing_TargetList(self):
        pass


