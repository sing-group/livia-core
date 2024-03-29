import random
from logging import Logger
from typing import Tuple

from numpy import ndarray

from livia.livia_property import livia_property
from livia.process.analyzer.CompositeFrameAnalyzer import CompositeFrameAnalyzer
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.FrameAnalyzerManager import FrameAnalyzerManager
from livia.process.analyzer.FrameAnalyzerMetadata import frame_analyzer
from livia.process.analyzer.NoChangeFrameAnalyzer import NoChangeFrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.analyzer.modification.SingleBoxFrameModification import SingleBoxFrameModification
from livia.process.analyzer import DEFAULT_BOX_COLOR, DEFAULT_BOX_THICKNESS

BOX_SIZE = 50


@frame_analyzer(id="random-square", name="Random square")
class RandomSquareFrameAnalyzer(CompositeFrameAnalyzer):
    def __init__(self, box_size: int = BOX_SIZE, box_thickness: int = DEFAULT_BOX_THICKNESS,
                 box_color: Tuple[int, int, int] = DEFAULT_BOX_COLOR, child: FrameAnalyzer = NoChangeFrameAnalyzer()):
        CompositeFrameAnalyzer.__init__(self, child)

        self.__x: int = 0
        self.__y: int = 0
        self.__box_thickness: int = box_thickness

        self.__box_size: int = box_size
        self.__box_color: Tuple[int, int, int] = box_color

        self.__logger: Logger = FrameAnalyzerManager.get_logger_for(self)

    @livia_property(id="box-color", name="Box color", default_value=DEFAULT_BOX_COLOR)
    def box_color(self) -> Tuple[int, int, int]:
        """The color of the box painted"""
        return self.__box_color

    @box_color.setter  # type: ignore
    def box_color(self, color: Tuple[int, int, int]):
        self.__box_color = color

    def _composite_analyze(self, num_frame: int, frame: ndarray,
                           child_modification: FrameModification) -> FrameModification:
        height = frame.shape[0]
        width = frame.shape[1]

        if height < self.__box_size or width < self.__box_size:
            return NoFrameModification()
        else:
            self.__y = random.randint(0, height - self.__box_size)
            self.__x = random.randint(0, width - self.__box_size)

            box = (self.__x, self.__y, self.__x + self.__box_size, self.__y + self.__box_size)

            # Tip: use a log format string like %(num_frame)d,%(box_x0)d,%(box_y0)d,%(box_x1)d,%(box_y1)d
            # to get CSV output from these log records
            self.__logger.info("Frame modification shown",
                               extra={"num_frame": num_frame, "box_x0": box[0], "box_y0": box[1], "box_x1": box[2],
                                      "box_y1": box[3]})

            return SingleBoxFrameModification(box, self.__box_color, self.__box_thickness)
