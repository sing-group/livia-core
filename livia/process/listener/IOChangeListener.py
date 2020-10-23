from livia.process.listener.EventListener import EventListener
from livia.process.listener.IOChangeEvent import IOChangeEvent


class IOChangeListener(EventListener):
    def input_changed(self, event: IOChangeEvent):
        pass

    def output_changed(self, event: IOChangeEvent):
        pass
