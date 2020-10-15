from abc import abstractmethod
from typing import Optional

from numpy import ndarray

from livia.livia_property import livia_property
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.object_detection import DEFAULT_BOX_COLOR
from livia.process.analyzer.object_detection import FrameObjectDetection
from livia.process.analyzer.object_detection import ObjectDetectionFrameModification


class ObjectDetectorFrameAnalyzer(CompositeFrameAnalyzer):
    def __init__(self,
                 score_threshold: Optional[float] = None,
                 box_color: (int, int, int) = DEFAULT_BOX_COLOR,
                 child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        super().__init__(child)
        self._score_threshold: Optional[float] = score_threshold
        self._box_color: (int, int, int) = box_color

    @livia_property
    def box_color(self) -> (int, int, int):
        return self._box_color

    @box_color.setter
    def box_color(self, box_color: (int, int, int)):
        self._box_color = box_color

    @livia_property
    def score_threshold(self) -> Optional[float]:
        return self._score_threshold

    @score_threshold.setter
    def score_threshold(self, score_threshold: Optional[float]):
        self._score_threshold = score_threshold

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> ObjectDetectionFrameModification:
        return self._create_modification(self._detect_objects(num_frame, frame), child_modification)

    @abstractmethod
    def _detect_objects(self, num_frame: int, frame: ndarray) -> FrameObjectDetection:
        raise NotImplementedError()

    def _create_modification(self, objects: FrameObjectDetection,
                             child_modification: FrameModification) -> ObjectDetectionFrameModification:
        return ObjectDetectionFrameModification(objects, self._score_threshold, self._box_color, child_modification)
