from __future__ import annotations

from typing import TYPE_CHECKING

from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer

if TYPE_CHECKING:
    from livia.process.analyzer.AnalyzerFrameProcessor import AnalyzerFrameProcessor


class FrameAnalyzerChangeEvent:
    def __init__(self, processor: AnalyzerFrameProcessor, new: FrameAnalyzer, old: FrameAnalyzer):
        self.__processor: AnalyzerFrameProcessor = processor
        self.__new: FrameAnalyzer = new
        self.__old: FrameAnalyzer = old

    def processor(self) -> AnalyzerFrameProcessor:
        return self.__processor

    def new(self) -> FrameAnalyzer:
        return self.__new

    def old(self) -> FrameAnalyzer:
        return self.__old
