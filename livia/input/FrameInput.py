from abc import ABC, abstractmethod
from typing import Optional, Tuple

from numpy import ndarray


class FrameInput(ABC):
    def play(self):
        pass

    @abstractmethod
    def next_frame(self) -> Tuple[Optional[int], Optional[ndarray]]:
        raise NotImplementedError()

    @abstractmethod
    def get_fps(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_frame_size(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def close(self):
        pass
