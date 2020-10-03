from numpy import ndarray

from livia.core.input.FrameInput import FrameInput
from livia.core.output.FrameOutput import FrameOutput
from livia.core.process.FrameProcessor import FrameProcessor
from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer


class AnalyzerFrameProcessor(FrameProcessor):
    def __init__(self, input: FrameInput, output: FrameOutput, frame_analyzer: FrameAnalyzer, daemon: bool = True):
        super().__init__(input, output, daemon)
        self._frame_analyzer = frame_analyzer

    def manipulate_frame(self, num_frame: int, frame: ndarray) -> ndarray:
        modification = self._frame_analyzer.analyze(num_frame, frame)

        return modification.modify(num_frame, frame)
