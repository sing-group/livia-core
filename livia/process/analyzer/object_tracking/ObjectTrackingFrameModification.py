from typing import List, Tuple

import cv2
from numpy import ndarray

from livia.process.analyzer import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS
from livia.process.analyzer.modification.CompositeFrameModification import CompositeFrameModification
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.analyzer.object_detection.DetectedObject import DetectedObject
from livia.process.analyzer.object_tracking.TrackedObjects import TrackedObjects


class ObjectTrackingFrameModification(CompositeFrameModification):
    def __init__(self,
                 tracked_objects: TrackedObjects,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
                 box_thickness: int = DEFAULT_BOX_THICKNESS,
                 show_scores: bool = False,
                 show_class_names: bool = False,
                 child: FrameModification = NoFrameModification()):
        super().__init__(child)
        self._tracked_objects: TrackedObjects = tracked_objects
        self._box_color: Tuple[int, int, int] = box_color
        self._box_thickness: int = box_thickness
        self._show_scores: bool = show_scores
        self._show_class_names: bool = show_class_names

    def _composite_modify(self, num_frame: int, frame: ndarray) -> ndarray:
        self._pre_draw(num_frame, frame)

        for detected_object in self._get_objects_to_draw(num_frame, frame):
            self._draw_object(num_frame, frame, detected_object)

        self._post_draw(num_frame, frame)

        return frame

    def _get_objects_to_draw(self, num_frame: int, frame: ndarray) -> List[DetectedObject]:
        return [tracked_object.last_frame_consensus for tracked_object in self._tracked_objects.tracked_objects if
                tracked_object.last_frame_consensus is not None]

    def _pre_draw(self, num_frame: int, frame: ndarray):
        pass

    def _post_draw(self, num_frame: int, frame: ndarray):
        pass

    def _draw_object(self, num_frame: int, frame: ndarray, detected_object: DetectedObject):
        location = detected_object.location

        if self._show_scores and detected_object.has_score():
            cv2.putText(frame,
                        str(detected_object.score)[1:5],
                        location.adjust_coord0(),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)

        if self._show_class_names and detected_object.has_class_name():
            cv2.putText(frame,
                        detected_object.class_name,
                        location.adjust_coord0(lambda x: x + 50, lambda y: y + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)

        cv2.rectangle(frame, location.adjust_coord0(), location.adjust_coord1(), self._box_color, self._box_thickness)
