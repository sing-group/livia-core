import numpy

from livia.core.process.analyzer.FrameAnalyzerMetadata import frame_analyzer, frame_analyzer_property
from livia.core.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.core.process.analyzer.modification.FrameModification import FrameModification


@frame_analyzer(name="No change")
class NoChangeFrameAnalyzer(FrameAnalyzer):
    def analyze(self, frame: numpy.ndarray) -> FrameModification:
        return NoFrameModification()

    @frame_analyzer_property
    def name(self):
        print("getter")
        return "Hello"

    @name.setter
    def name(self, name: str):
        print("setter")
        pass

    @property
    def surname(self):
        print("getter surname")
        return "Hello"

    @surname.setter
    def surname(self, surname: str):
        print("setter surname")
        pass
