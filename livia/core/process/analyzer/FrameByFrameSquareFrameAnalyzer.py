from numpy import ndarray

from livia.core.livia_property import livia_property
from livia.core.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.core.process.analyzer.FrameAnalyzerMetadata import frame_analyzer
from livia.core.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.core.process.analyzer.modification.FrameModification import FrameModification
from livia.core.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.core.process.analyzer.modification.SingleBoxFrameModification import SingleBoxFrameModification
from livia.core.process.analyzer.object_detection import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS

X_STEP = 5
Y_STEP = 5
BOX_SIZE = 50


@frame_analyzer(id="square", name="Frame by frame square")
class FrameByFrameSquareFrameAnalyzer(CompositeFrameAnalyzer):
    def __init__(self, x_step: int = X_STEP, y_step: int = Y_STEP, box_size: int = BOX_SIZE,
                 box_thickness: int = DEFAULT_BOX_THICKNESS, box_color: (int, int, int) = DEFAULT_BOX_COLOR,
                 child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        super().__init__(child)

        self.__x = 0
        self.__y = 0
        self.__x_step: int = x_step
        self.__y_step: int = y_step
        self.__box_thickness: int = box_thickness

        self.__box_size: int = box_size
        self.__box_color: (int, int, int) = box_color

    @livia_property(id="box-color", name="Box color")
    def box_color(self) -> (int, int, int):
        """The color of the box painted"""
        return self.__box_color

    @box_color.setter
    def box_color(self, color: (int, int, int)):
        self.__box_color = color

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> FrameModification:
        height = frame.shape[0]
        width = frame.shape[1]

        if height < self.__box_size or width < self.__box_size:
            return NoFrameModification()
        else:
            self.__y, self.__y_step = self.__adjust_dimension(self.__y, self.__y_step, height)
            self.__x, self.__x_step = self.__adjust_dimension(self.__x, self.__x_step, width)

            box = (self.__x, self.__y, self.__x + self.__box_size, self.__y + self.__box_size)

            return SingleBoxFrameModification(box, self.__box_color, self.__box_thickness)

    def __adjust_dimension(self, current: int, step: int, max: int) -> (int, int):
        new_position = current + step

        if new_position < 0 or new_position > max - self.__box_size:
            step = -step
            new_position = current + step

        return new_position, step
