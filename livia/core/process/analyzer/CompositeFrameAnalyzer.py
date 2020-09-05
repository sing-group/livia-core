from abc import abstractmethod

from numpy import ndarray

from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.core.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.core.process.analyzer.modification.FrameModification import FrameModification


class CompositeFrameAnalyzer(FrameAnalyzer):
    def __init__(self, child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        self._child = child

    def analyze(self, frame: ndarray) -> FrameModification:
        return self._composite_analyze(frame, self._child.analyze(frame))

    @abstractmethod
    def _composite_analyze(self, frame: ndarray, modification: FrameModification) -> FrameModification:
        pass

    @property
    def child(self) -> FrameAnalyzer:
        return self._child

    @child.setter
    def child(self, child: FrameAnalyzer):
        self._child = child
