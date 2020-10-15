from abc import ABC, abstractmethod
from collections import deque

from numpy import ndarray

from livia.process.analyzer.modification.FrameModification import FrameModification


class BoxTracker(ABC):
    def __init__(self, frames_window_size: int = 10):
        self.__frames_window = deque([], frames_window_size)

    def process_frame(self, frame: ndarray, frame_modification: FrameDetection) -> FrameModification:
        new_frame_modification = self._calculate_boxes(frame, frame_modification)

        self.__frames_window.append((frame_modification, new_frame_modification))

        return new_frame_modification

    @abstractmethod
    def _calculate_boxes(self, frame: ndarray, frame_modification: FrameModification) -> FrameModification:
        raise NotImplementedError()
