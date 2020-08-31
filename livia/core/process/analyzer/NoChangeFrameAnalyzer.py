from numpy import ndarray

from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.core.process.analyzer.modification.FrameModification import FrameModification
from livia.core.process.analyzer.modification.NoFrameModification import NoFrameModification


class NoChangeFrameAnalyzer(FrameAnalyzer):
    def analyze(self, frame: ndarray) -> FrameModification:
        return NoFrameModification()
