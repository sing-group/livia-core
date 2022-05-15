from abc import abstractmethod
from typing import Tuple

from numpy import ndarray

from livia.benchmarking.TimeLogger import TimeLogger
from livia.livia_property import livia_property
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.classification import ClassificationFrameModification, DEFAULT_TEXT_COLOR
from livia.process.analyzer.classification.Classification import Classification
from livia.process.analyzer.modification.FrameModification import FrameModification


class ClassificationFrameAnalyzer(CompositeFrameAnalyzer):
    def __init__(self,
                 info_color: Tuple[int, int, int] = DEFAULT_TEXT_COLOR,
                 child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        CompositeFrameAnalyzer.__init__(self, child)

        self._info_color: Tuple[int, int, int] = info_color
        self._tl_classification: TimeLogger = TimeLogger("Classification", self)

    @livia_property(id="info-color", name="Information color", default_value=DEFAULT_TEXT_COLOR)
    def info_color(self) -> Tuple[int, int, int]:
        return self._info_color

    @info_color.setter
    def info_color(self, info_color: Tuple[int, int, int]):
        self._info_color = info_color

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> FrameModification:
        with self._tl_classification:
            classify = self._classify(num_frame, frame)

        return self._create_modification(classify, child_modification)

    @abstractmethod
    def _classify(self, num_frame, frame: ndarray) -> Classification:
        raise NotImplementedError()

    def _create_modification(self, classification: Classification,
                             child_modification: FrameModification) -> ClassificationFrameModification:
        return ClassificationFrameModification(classification, self._info_color, child_modification)
