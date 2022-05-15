from abc import abstractmethod, ABC
from copy import copy
from typing import Tuple, Optional, Union

from numpy import ndarray
from numpy.typing import NDArray

from livia.benchmarking.TimeLogger import TimeLogger
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
        self.__tl_detect_objects = TimeLogger("Detect objects", self)
        self.__tl_group_intra_frame = TimeLogger("Group intra frame", self)
        self.__tl_group_inter_frame = TimeLogger("Group inter frame", self)

    @livia_property(id="window-size", name="Window size", default_value=DEFAULT_WINDOW_SIZE)
    def window_size(self) -> int:
        return self._window_size

    @window_size.setter  # type: ignore
    def window_size(self, window_size: int = 50):
        self._window_size = window_size

    @livia_property(id="box-thickness", name="Box thickness", default_value=5)
    def box_thickness(self) -> int:
        return self._box_thickness

    @box_thickness.setter  # type: ignore
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

    def process_frame(self, num_frame: int, frame: Union[ndarray, NDArray], update: bool = True) -> TrackedObjects:
        with self.__tl_detect_objects:
            objects_in_frame = self._detect_objects_in_frame(num_frame, frame)

        with self.__tl_group_intra_frame:
            intra_frame_detections = self._group_intra_frame_objects(num_frame, objects_in_frame)

        with self.__tl_group_inter_frame:
            tracked_objects = self._tracked_objects if update else copy(self._tracked_objects)
            tracked_objects = self._group_inter_frame_objects(num_frame, intra_frame_detections, tracked_objects)

        return tracked_objects

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> ObjectTrackingFrameModification:
        self._tracked_objects = self.process_frame(num_frame, frame)

        return self._create_modification(self._tracked_objects, child_modification)

    @abstractmethod
    def _detect_objects_in_frame(self, num_frame: int, frame: Union[ndarray, NDArray]) -> FrameObjectDetection:
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
