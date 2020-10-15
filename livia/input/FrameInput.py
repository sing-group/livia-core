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
    def get_fps(self) -> int:
        pass

    def get_frame_size(self) -> (int, int):
        return self.__x_frame, self.__y_frame

    def close(self):
        pass
