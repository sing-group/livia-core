from abc import ABC, abstractmethod

from numpy import ndarray


class FrameOutput(ABC):
    def __init__(self):
        self.created = False

    @abstractmethod
    def show_frame(self, frame: ndarray):
        pass

    @abstractmethod
    def close_output(self):
        pass
