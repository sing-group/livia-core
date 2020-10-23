from livia.process.listener.EventListener import EventListener
from livia.process.listener.ProcessChangeEvent import ProcessChangeEvent


class ProcessChangeListener(EventListener):
    def started(self, event: ProcessChangeEvent):
        pass

    def stopped(self, event: ProcessChangeEvent):
        pass

    def finished(self, event: ProcessChangeEvent):
        pass

    def paused(self, event: ProcessChangeEvent):
        pass

    def resumed(self, event: ProcessChangeEvent):
        pass
