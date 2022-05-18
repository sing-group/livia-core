from typing import List, Optional, Tuple

import cv2
from numpy import ndarray

from livia.process.analyzer import DEFAULT_BOX_THICKNESS
from livia.process.analyzer.modification.CompositeFrameModification import CompositeFrameModification
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.analyzer.object_detection.DetectedObject import DetectedObject

DEFAULT_SHOW_SCORE: bool = True
DEFAULT_SHOW_CLASS_NAME: bool = True


class ObjectTrackingAndClassifyingFrameModification(CompositeFrameModification):
    def __init__(self,
                 classifications: Optional[
                     List[Tuple[DetectedObject, Optional[Tuple[Optional[str], Optional[float]]]]]],
                 box_thickness: int = DEFAULT_BOX_THICKNESS,
                 show_score: bool = DEFAULT_SHOW_SCORE,
                 show_class_name: bool = DEFAULT_SHOW_CLASS_NAME,
                 child: FrameModification = NoFrameModification()):
        super().__init__(child)

        self._classifications: Optional[
            List[Tuple[DetectedObject, Optional[Tuple[Optional[str], Optional[float]]]]]] = classifications
        self._box_thickness: int = box_thickness
        self._show_score: bool = show_score
        self._show_class_name: bool = show_class_name

    def _composite_modify(self, num_frame: int, frame: ndarray) -> ndarray:
        if self._classifications is not None:
            for detected_object, classification in self._classifications:
                self._draw_object(num_frame, frame, detected_object, classification)

        return frame

    def _draw_object(self, num_frame: int, frame: ndarray, detected_object: DetectedObject,
                     classification: Optional[Tuple[Optional[str], Optional[float]]]):
        if classification is not None:
            class_name = classification[0]
            score = classification[1]
        else:
            class_name = None
            score = None

        location = detected_object.location

        color = [255, 0, 0] if score is None else [0, round(255 * (1 - score)), round(255 * score)]

        cv2.rectangle(frame, location.adjust_coord0(), location.adjust_coord1(), color, self._box_thickness)

        label = None
        if self._show_score and score is not None:
            label = f"{score:6.2%}"

        if self._show_class_name and detected_object.has_class_name():
            label = class_name if label is None else f"{class_name}: {label}"

        if label is not None:
            cv2.putText(frame, label, location.adjust_coord0(lambda x: x + 20, lambda y: y + 20),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        fontScale=1,
                        color=color,
                        thickness=1)
