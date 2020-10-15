import cv2
from numpy import ndarray

from livia.process.analyzer.modification.CompositeFrameModification import CompositeFrameModification
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.analyzer.object_detection import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS


class SingleBoxFrameModification(CompositeFrameModification):
    def __init__(self, box: (int, int, int, int),
                 box_color: (int, int, int) = DEFAULT_BOX_COLOR,
                 box_thickness: int = DEFAULT_BOX_THICKNESS,
                 child: FrameModification = NoFrameModification()):
        super().__init__(child)
        self.__box: (int, int, int, int) = box
        self.__box_color: (int, int, int) = box_color
        self.__box_thickness: int = box_thickness

    def _composite_modify(self, num_frame: int, frame: ndarray) -> ndarray:
        cv2.rectangle(frame, (self.__box[0], self.__box[1]), (self.__box[2], self.__box[3]), self.__box_color,
                      self.__box_thickness)
        return frame
