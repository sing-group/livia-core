from livia.process.analyzer.listener.FrameAnalyzerChangeEvent import FrameAnalyzerChangeEvent
from livia.process.listener import EventListener


class FrameAnalyzerChangeListener(EventListener):
    def analyzer_changed(self, event: FrameAnalyzerChangeEvent) -> None:
        pass
