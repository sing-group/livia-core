from abc import ABC, abstractmethod
from copy import copy
from typing import List, Tuple, Optional, TypeVar, Generic

from numpy import ndarray

from livia.benchmarking.TimeLogger import TimeLogger
from livia.livia_property import livia_property
from livia.process.analyzer import DEFAULT_WINDOW_SIZE, DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.object_detection.DetectedObject import DetectedObject
from livia.process.analyzer.object_detection.FrameObjectDetection import FrameObjectDetection
from livia.process.analyzer.object_tracking.FrameDetectedObjectGroups import FrameDetectedObjectGroups
from livia.process.analyzer.object_tracking.TrackedObject import TrackedObject
from livia.process.analyzer.object_tracking.TrackedObjects import TrackedObjects
from livia.process.analyzer.object_tracking.classification.ObjectTrackingAndClassifyingFrameModification import \
    ObjectTrackingAndClassifyingFrameModification

T = TypeVar("T")


class ObjectTrackingAndClassifyingFrameAnalyzer(CompositeFrameAnalyzer, ABC, Generic[T]):
    def __init__(
            self,
            window_size: int = DEFAULT_WINDOW_SIZE,
            box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
            box_thickness: int = DEFAULT_BOX_THICKNESS,
            show_scores: bool = False,
            show_class_names: bool = False,
            child: FrameAnalyzer = NoChangeFrameAnalyzer()
    ):
        if window_size <= 0:
            raise ValueError("window_size must be a positive number")

        CompositeFrameAnalyzer.__init__(self, child)

        self._box_color: Tuple[int, int, int] = box_color
        self._box_thickness: int = box_thickness
        self._show_scores: bool = show_scores
        self._show_class_names: bool = show_class_names
        self._window_size: int = window_size

        self._tracked_objects: TrackedObjects = TrackedObjects(window_size=self._window_size)

        self._tl_process_frame = TimeLogger("Process frame", self)

        self._tl_preprocess_frame = TimeLogger("Preprocess frame", self)
        self._tl_tracking = TimeLogger("Tracking", self)
        self._tl_classify = TimeLogger("Classify", self)
        self._tl_build_modification = TimeLogger("Build modification", self)

        self._tl_detect_objects = TimeLogger("Detect objects", self)
        self._tl_group_intra_frame = TimeLogger("Group intra frame", self)
        self._tl_group_inter_frame = TimeLogger("Group inter frame", self)

    @livia_property(id="window-size", name="Window size", default_value=DEFAULT_WINDOW_SIZE)
    def window_size(self) -> int:
        return self._window_size

    @window_size.setter  # type: ignore
    def window_size(self, window_size: int = DEFAULT_WINDOW_SIZE):
        if self._window_size != window_size:
            if window_size <= 0:
                raise ValueError("window_size must be a positive number")

            self._window_size = window_size
            self._tracked_objects.window_size = window_size

    @livia_property(id="box-thickness", name="Box thickness", default_value=DEFAULT_BOX_THICKNESS)
    def box_thickness(self) -> int:
        return self._box_thickness

    @box_thickness.setter  # type: ignore
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
                           child_modification: FrameModification) -> ObjectTrackingAndClassifyingFrameModification:
        with self._tl_process_frame:
            with self._tl_preprocess_frame:
                preprocessed_frame = self.preprocess_frame(num_frame, frame)

            with self._tl_tracking:
                tracked_objects = self.track_objects(num_frame, preprocessed_frame)

            with self._tl_classify:
                classification = self._classify_objects(num_frame, preprocessed_frame, tracked_objects)

            with self._tl_build_modification:
                return self.build_modification(num_frame, frame, tracked_objects, classification, child_modification)

    def preprocess_frame(self, num_frame: int, frame: ndarray) -> T:
        return frame

    def track_objects(self, num_frame: int, frame: T, update: bool = True) -> TrackedObjects:
        with self._tl_detect_objects:
            objects_in_frame = self._detect_objects_in_frame(num_frame, frame)

        with self._tl_group_intra_frame:
            intra_frame_detections = self._group_intra_frame_objects(num_frame, objects_in_frame)

        with self._tl_group_inter_frame:
            tracked_objects = self._tracked_objects if update else copy(self._tracked_objects)
            tracked_objects = self._group_inter_frame_objects(num_frame, intra_frame_detections, tracked_objects)

        return tracked_objects

    @abstractmethod
    def _detect_objects_in_frame(self, num_frame: int, frame: T) -> FrameObjectDetection:
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

    @abstractmethod
    def _classify_objects(
            self, num_frame: int, frame: T, tracked_objects: TrackedObjects
    ) -> List[Tuple[TrackedObject, DetectedObject, Optional[Tuple[Optional[str], Optional[float]]]]]:
        raise NotImplementedError()

    def build_modification(
            self,
            num_frame: int,
            frame: ndarray,
            tracked_objects: Optional[TrackedObjects],
            classifications: Optional[List[Tuple[DetectedObject, Optional[Tuple[Optional[str], Optional[float]]]]]],
            child_modification: FrameModification
    ) -> ObjectTrackingAndClassifyingFrameModification:
        raise NotImplementedError()
