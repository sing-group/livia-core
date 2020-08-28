from abc import ABC, abstractmethod

from numpy import ndarray


class FrameInput(ABC):
    def __init__(self):
        self.__x_frame = self.__y_frame = 0
        self.__cap = None

    @abstractmethod
    def next_frame(self) -> ndarray:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_fps(self) -> int:
        pass

    @abstractmethod
    def get_frame_size(self) -> int:
        return self.x_frame, self.y_frame
