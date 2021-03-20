from livia.process.listener.EventListener import EventListener
from livia.process.listener.ProcessChangeEvent import ProcessChangeEvent


class ProcessChangeListener(EventListener):
    def started(self, event: ProcessChangeEvent) -> None:
        pass

    def stopped(self, event: ProcessChangeEvent) -> None:
        pass

    def finished(self, event: ProcessChangeEvent) -> None:
        pass

    def paused(self, event: ProcessChangeEvent) -> None:
        pass

    def resumed(self, event: ProcessChangeEvent) -> None:
        pass

    def frame_inputted(self, event: ProcessChangeEvent) -> None:
        pass

    def frame_outputted(self, event: ProcessChangeEvent) -> None:
        pass
