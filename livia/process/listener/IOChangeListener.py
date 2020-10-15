from livia.process.listener import IOChangeEvent


class IOChangeListener:
    def input_changed(self, event: IOChangeEvent):
        pass

    def output_changed(self, event: IOChangeEvent):
        pass
