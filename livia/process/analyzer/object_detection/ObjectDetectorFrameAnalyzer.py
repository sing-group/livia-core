from abc import abstractmethod
from typing import Tuple

from numpy import ndarray

from livia.livia_property import livia_property
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.HasThreshold import HasThreshold
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.object_detection import DEFAULT_BOX_COLOR
from livia.process.analyzer.object_detection.FrameObjectDetection import FrameObjectDetection
from livia.process.analyzer.object_detection.ObjectDetectionFrameModification import ObjectDetectionFrameModification


class ObjectDetectorFrameAnalyzer(CompositeFrameAnalyzer, HasThreshold):
    def __init__(self,
                 initial_threshold: float = 0.0,
                 min_threshold: float = 0.0,
                 max_threshold: float = 1.0,
                 threshold_step: float = 0.01,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
                 child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        HasThreshold.__init__(initial_threshold, min_threshold, max_threshold, threshold_step)
        CompositeFrameAnalyzer.__init__(self, child)

        self._box_color: Tuple[int, int, int] = box_color

    @livia_property(id="box-color", name="Box color")
    def box_color(self) -> Tuple[int, int, int]:
        return self._box_color

    @box_color.setter  # type: ignore
    def box_color(self, box_color: Tuple[int, int, int]):
        self._box_color = box_color

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> ObjectDetectionFrameModification:
        return self._create_modification(self._detect_objects(num_frame, frame), child_modification)

    @abstractmethod
    def _detect_objects(self, num_frame: int, frame: ndarray) -> FrameObjectDetection:
        raise NotImplementedError()

    def _create_modification(self, objects: FrameObjectDetection,
                             child_modification: FrameModification) -> ObjectDetectionFrameModification:
        return ObjectDetectionFrameModification(objects, self.threshold, self._box_color, child_modification)
