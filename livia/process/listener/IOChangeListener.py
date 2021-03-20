from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.listener.EventListener import EventListener
from livia.process.listener.IOChangeEvent import IOChangeEvent


class IOChangeListener(EventListener):
    def input_changed(self, event: IOChangeEvent[FrameInput]) -> None:
        pass

    def output_changed(self, event: IOChangeEvent[FrameOutput]) -> None:
        pass
