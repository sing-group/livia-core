from numpy import ndarray

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.FrameProcessor import FrameProcessor


class NoChangeFrameProcessor(FrameProcessor):
    def __init__(self, input: FrameInput, output: FrameOutput, daemon: bool = True):
        super().__init__(input, output, daemon)

    def _manipulate_frame(self, frame: ndarray) -> ndarray:
        return frame
