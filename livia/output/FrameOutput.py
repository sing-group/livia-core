from abc import ABC, abstractmethod

from numpy import ndarray


class FrameOutput(ABC):
    @abstractmethod
    def show_frame(self, frame: ndarray):
        pass

    def close(self):
        pass
