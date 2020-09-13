from abc import ABC, abstractmethod

from numpy import ndarray


class FrameModification(ABC):
    @abstractmethod
    def modify(self, num_frame: int, frame: ndarray) -> ndarray:
        raise NotImplementedError()
