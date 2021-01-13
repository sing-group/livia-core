from abc import ABC, abstractmethod

from numpy import ndarray


class FrameOutput(ABC):
    @abstractmethod
    def output_frame(self, num_frame: int, frame: ndarray):
        pass

    def close(self):
        pass
