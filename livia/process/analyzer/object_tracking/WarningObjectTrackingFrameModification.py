from typing import Tuple

import cv2
from numpy import ndarray

from livia.process.analyzer import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.analyzer.object_tracking.ObjectTrackingFrameModification import ObjectTrackingFrameModification
from livia.process.analyzer.object_tracking.TrackedObjects import TrackedObjects


class WarningObjectTrackingFrameModification(ObjectTrackingFrameModification):
    def __init__(self,
                 tracked_objects: TrackedObjects,
                 show_warning: bool = False,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR,
                 box_thickness: int = DEFAULT_BOX_THICKNESS,
                 show_scores: bool = False,
                 show_class_names: bool = False,
                 child: FrameModification = NoFrameModification()):
        super().__init__(tracked_objects, box_color, box_thickness, show_scores, show_class_names,
                         child)

        self._show_warning: bool = show_warning

    def _post_draw(self, num_frame: int, frame: ndarray) -> None:
        if self._show_warning:
            cv2.rectangle(frame, (0, 0), (frame.shape[1] - 1, frame.shape[0] - 1), (0, 0, 255), self._box_thickness)
