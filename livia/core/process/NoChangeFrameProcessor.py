from numpy import ndarray

from livia.core.input.FrameInput import FrameInput
from livia.core.output.FrameOutput import FrameOutput
from livia.core.process.FrameProcessor import FrameProcessor


class NoChangeFrameProcessor(FrameProcessor):
    def __init__(self, input: FrameInput, output: FrameOutput, daemon: bool = True):
        super().__init__(input, output, daemon)

    def manipulate_frame(self, num_frame: int, frame: ndarray) -> ndarray:
        return frame
