from abc import ABC, abstractmethod

from numpy import ndarray


class FrameModification(ABC):
    @abstractmethod
    def modify(self, frame: ndarray, *args) -> ndarray:
        pass
