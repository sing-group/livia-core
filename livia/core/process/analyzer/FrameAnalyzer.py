from abc import ABC, abstractmethod

from numpy import ndarray

from livia.core.process.analyzer.modification.FrameModification import FrameModification


class FrameAnalyzer(ABC):
    @abstractmethod
    def analyze(self, num_frame: int, frame: ndarray) -> FrameModification:
        pass
