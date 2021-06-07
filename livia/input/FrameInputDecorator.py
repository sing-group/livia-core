from abc import ABC, abstractmethod
from typing import Tuple, Optional

from numpy import ndarray

from livia.input.FrameInput import FrameInput


class FrameInputDecorator(FrameInput, ABC):
    def __init__(self, decorated_input: FrameInput):
        super().__init__()

        self._decorated_input: FrameInput = decorated_input

    @property
    def decorated_input(self) -> FrameInput:
        return self._decorated_input

    def play(self) -> None:
        self._decorated_input.play()

    def get_current_frame(self) -> Optional[ndarray]:
        return self._decorated_input.get_current_frame()

    def get_current_frame_index(self) -> Optional[int]:
        return self._decorated_input.get_current_frame_index()

    def next_frame(self) -> Tuple[Optional[int], Optional[ndarray]]:
        next_frame = self._decorated_input.next_frame()

        return self._manipulate_frame(next_frame)

    def get_fps(self) -> int:
        return self._decorated_input.get_fps()

    def get_frame_size(self) -> Tuple[int, int]:
        return self._decorated_input.get_frame_size()

    @abstractmethod
    def _manipulate_frame(self, frame: Tuple[Optional[int], Optional[ndarray]]) -> \
            Tuple[Optional[int], Optional[ndarray]]:
        raise NotImplementedError()

    def close(self) -> None:
        self._decorated_input.close()
