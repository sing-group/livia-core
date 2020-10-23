from typing import Optional, List, Tuple

import cv2
from numpy import ndarray

from livia.process.analyzer.modification.CompositeFrameModification import CompositeFrameModification
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.analyzer.object_detection import DEFAULT_BOX_COLOR
from livia.process.analyzer.object_detection.DetectedObject import DetectedObject
from livia.process.analyzer.object_detection.FrameObjectDetection import FrameObjectDetection


class ObjectDetectionFrameModification(CompositeFrameModification):
    def __init__(self,
                 frame_detection: FrameObjectDetection,
                 score_threshold: Optional[float] = None,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
                 child: FrameModification = NoFrameModification()):
        super().__init__(child)
        self._frame_detection: FrameObjectDetection = frame_detection
        self._score_threshold: Optional[float] = score_threshold
        self._box_color: Tuple[int, int, int] = box_color

    def _composite_modify(self, num_frame: int, frame: ndarray) -> ndarray:
        self._pre_draw(num_frame, frame)

        for detected_object in self._get_objects_to_draw(num_frame, frame):
            self._draw_object(num_frame, frame, detected_object)

        self._post_draw(num_frame, frame)

        return frame

    def _get_objects_to_draw(self, num_frame: int, frame: ndarray) -> List[DetectedObject]:
        if self._score_threshold is None:
            return self._frame_detection.objects
        else:
            return [detected_object for detected_object in self._frame_detection.objects if
                    detected_object.has_score() and detected_object.score >= self._score_threshold] # type: ignore

    def _pre_draw(self, num_frame: int, frame: ndarray):
        pass

    def _post_draw(self, num_frame: int, frame: ndarray):
        pass

    def _draw_object(self, num_frame: int, frame: ndarray, detected_object: DetectedObject):
        location = detected_object.location

        if detected_object.has_score():
            cv2.putText(frame,
                        str(detected_object.score)[1:5],
                        location.adjust_coord0(),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)

        if detected_object.has_class_name():
            cv2.putText(frame,
                        detected_object.class_name,
                        location.adjust_coord0(lambda x: x + 50, lambda y: y + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)

        cv2.rectangle(frame, location.adjust_coord0(), location.adjust_coord1(), self._box_color, 5)
