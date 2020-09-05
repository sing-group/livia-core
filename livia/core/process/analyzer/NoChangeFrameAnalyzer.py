import numpy

from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.core.process.analyzer.FrameAnalyzerMetadata import frame_analyzer
from livia.core.process.analyzer.modification.FrameModification import FrameModification
from livia.core.process.analyzer.modification.NoFrameModification import NoFrameModification


@frame_analyzer(name="No change")
class NoChangeFrameAnalyzer(FrameAnalyzer):
    def analyze(self, frame: numpy.ndarray) -> FrameModification:
        return NoFrameModification()
