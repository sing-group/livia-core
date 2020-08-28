from abc import ABC

from livia.core.input.FrameInput import FrameInput
from livia.core.output.FrameOutput import FrameOutput
from livia.core.process.FrameProcessor import FrameProcessor
from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer


class AnalyzerFrameProcessor(ABC, FrameProcessor):
    def __init__(self, frame_input: FrameInput, frame_output: FrameOutput, frame_analyzer: FrameAnalyzer):
        super().__init__(frame_input, frame_output)
        self._frame_analyzer = frame_analyzer
