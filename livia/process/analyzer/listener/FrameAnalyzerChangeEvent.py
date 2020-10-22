from livia.process.analyzer import FrameAnalyzer


class FrameAnalyzerChangeEvent:
    def __init__(self, processor, new: FrameAnalyzer, old: FrameAnalyzer):
        self.__processor = processor
        self.__new = new
        self.__old = old

    def processor(self):
        return self.__processor

    def new(self) -> FrameAnalyzer:
        return self.__new

    def old(self) -> FrameAnalyzer:
        return self.__old
