from abc import abstractmethod, ABC
from typing import Tuple, Optional

from numpy import ndarray

from livia.livia_property import livia_property
from livia.process.analyzer import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS, DEFAULT_WINDOW_SIZE
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.object_detection.FrameObjectDetection import FrameObjectDetection
from livia.process.analyzer.object_tracking.FrameDetectedObjectGroups import FrameDetectedObjectGroups
from livia.process.analyzer.object_tracking.ObjectTrackingFrameModification import ObjectTrackingFrameModification
from livia.process.analyzer.object_tracking.TrackedObjects import TrackedObjects


class ObjectTrackingFrameAnalyzer(CompositeFrameAnalyzer, ABC):
    def __init__(self,
                 window_size: Optional[int] = DEFAULT_WINDOW_SIZE,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
                 box_thickness: int = DEFAULT_BOX_THICKNESS,
                 show_scores: bool = False,
                 show_class_names: bool = False,
                 child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        CompositeFrameAnalyzer.__init__(self, child)

        self._box_color: Tuple[int, int, int] = box_color
        self._box_thickness: int = box_thickness
        self._show_scores: bool = show_scores
        self._show_class_names: bool = show_class_names
        self._window_size: Optional[int] = window_size

        self._tracked_objects: TrackedObjects = TrackedObjects()

    @livia_property(id="window-size", name="Window size", default_value=DEFAULT_WINDOW_SIZE)
    def window_size(self) -> int:
        return self._window_size

    @window_size.setter
    def window_size(self, window_size: int = 50):
        self._window_size = window_size

    @livia_property(id="box-thickness", name="Box thickness", default_value=5)
    def box_thickness(self) -> int:
        return self._box_thickness

    @box_thickness.setter
    def box_thickness(self, box_thickness: int = 5):
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
                           child_modification: FrameModification) -> ObjectTrackingFrameModification:
        objects_in_frame = self._detect_objects_in_frame(num_frame, frame)
        intra_frame_detections = self._group_intra_frame_objects(num_frame, objects_in_frame)
        self._tracked_objects = self._group_inter_frame_objects(num_frame, intra_frame_detections,
                                                                self._tracked_objects)

        return self._create_modification(self._tracked_objects, child_modification)

    @abstractmethod
    def _detect_objects_in_frame(self, num_frame: int, frame: ndarray) -> FrameObjectDetection:
        raise NotImplementedError()

    @abstractmethod
    def _group_intra_frame_objects(self,
                                   num_frame: int,
                                   detection: FrameObjectDetection) -> FrameDetectedObjectGroups:
        raise NotImplementedError()

    @abstractmethod
    def _group_inter_frame_objects(self,
                                   num_frame: int,
                                   intra_frame_detection: FrameDetectedObjectGroups,
                                   tracked_objects: TrackedObjects) -> TrackedObjects:
        raise NotImplementedError()

    def _create_modification(self, tracked_objects: TrackedObjects,
                             child_modification: FrameModification) -> ObjectTrackingFrameModification:
        return ObjectTrackingFrameModification(tracked_objects, self._box_color, self._box_thickness, self._show_scores,
                                               self._show_class_names, child=child_modification)
