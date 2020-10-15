from numpy import ndarray

from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.FrameAnalyzerMetadata import frame_analyzer
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification


@frame_analyzer(id="no-change", name="No change")
class NoChangeFrameAnalyzer(FrameAnalyzer):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not NoChangeFrameAnalyzer.__instance:
            NoChangeFrameAnalyzer.__instance = super().__new__(cls, *args, **kwargs)

        return NoChangeFrameAnalyzer.__instance

    def analyze(self, num_frame: int, frame: ndarray) -> FrameModification:
        return NoFrameModification()
