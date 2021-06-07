from abc import ABC, abstractmethod
from typing import Optional, Tuple

from numpy import ndarray


class FrameInput(ABC):
    def play(self) -> None:
        pass

    @abstractmethod
    def get_current_frame(self) -> Optional[ndarray]:
        raise NotImplementedError()

    @abstractmethod
    def get_current_frame_index(self) -> Optional[int]:
        raise NotImplementedError()

    def get_current_msec(self) -> Optional[int]:
        frame_index = self.get_current_frame_index()

        return None if frame_index is None else round(frame_index * (1 / self.get_fps()) * 1000)

    @abstractmethod
    def next_frame(self) -> Tuple[Optional[int], Optional[ndarray]]:
        raise NotImplementedError()

    @abstractmethod
    def get_fps(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_frame_size(self) -> Tuple[int, int]:
        raise NotImplementedError()

    def close(self) -> None:
        pass
