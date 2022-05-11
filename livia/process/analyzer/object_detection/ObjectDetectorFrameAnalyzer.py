from abc import abstractmethod
from typing import Tuple

from numpy import ndarray

from livia.livia_property import livia_property
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.HasThreshold import HasThreshold
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS
from livia.process.analyzer.object_detection.FrameObjectDetection import FrameObjectDetection
from livia.process.analyzer.object_detection.ObjectDetectionFrameModification import ObjectDetectionFrameModification


class ObjectDetectorFrameAnalyzer(CompositeFrameAnalyzer, HasThreshold):
    def __init__(self,
                 initial_threshold: float = 0.0,
                 min_threshold: float = 0.0,
                 max_threshold: float = 1.0,
                 threshold_step: float = 0.01,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
                 box_thickness: int = DEFAULT_BOX_THICKNESS,
                 show_scores: bool = False,
                 show_class_names: bool = False,
                 child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        HasThreshold.__init__(self, initial_threshold, min_threshold, max_threshold, threshold_step)
        CompositeFrameAnalyzer.__init__(self, child)

        self._box_color: Tuple[int, int, int] = box_color
        self._box_thickness: int = box_thickness
        self._show_scores: bool = show_scores
        self._show_class_names: bool = show_class_names

    @livia_property(id="box-thickness", name="Box thickness", default_value=DEFAULT_BOX_THICKNESS)
    def box_thickness(self) -> int:
        return self._box_thickness

    @box_thickness.setter
    def box_thickness(self, box_thickness: int):
        self._box_thickness = box_thickness

    @livia_property(id="box-color", name="Box color", default_value=DEFAULT_BOX_COLOR)
    def box_color(self) -> Tuple[int, int, int]:
        return self._box_color

    @box_color.setter  # type: ignore
    def box_color(self, box_color: Tuple[int, int, int]):
        self._box_color = box_color

    @livia_property(id="show-scores", name="Show scores", default_value=False)
    def show_scores(self) -> bool:
        return self._show_scores

    @show_scores.setter  # type: ignore
    def show_scores(self, show_scores: bool):
        self._show_scores = show_scores

    @livia_property(id="show-class-names", name="Show class names", default_value=False)
    def show_class_names(self) -> bool:
        return self._show_class_names

    @show_class_names.setter  # type: ignore
    def show_class_names(self, show_class_labels: bool):
        self._show_class_names = show_class_labels

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> ObjectDetectionFrameModification:
        return self._create_modification(self._detect_objects(num_frame, frame), child_modification)

    @abstractmethod
    def _detect_objects(self, num_frame: int, frame: ndarray) -> FrameObjectDetection:
        raise NotImplementedError()

    def _create_modification(self, objects: FrameObjectDetection,
                             child_modification: FrameModification) -> ObjectDetectionFrameModification:
        return ObjectDetectionFrameModification(objects, self.threshold,
                                                self._box_color, self._box_thickness,
                                                self._show_scores, self._show_class_names,
                                                child=child_modification)
