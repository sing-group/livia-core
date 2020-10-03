from livia.core.process.listener.ProcessChangeEvent import ProcessChangeEvent


class ProcessChangeListener:
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
