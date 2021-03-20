from livia.process.analyzer.listener.ThresholdChangeEvent import ThresholdChangeEvent
from livia.process.listener import EventListener


class ThresholdChangeListener(EventListener):
    def threshold_changed(self, event: ThresholdChangeEvent) -> None:
        pass
