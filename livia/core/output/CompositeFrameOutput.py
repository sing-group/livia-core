import numpy

from livia.core.output.FrameOutput import FrameOutput


class CompositeFrameOutput(FrameOutput):
    def __init__(self, *outs):
        super().__init__()

        self.frame_outputs = []

        for out in outs:
            if isinstance(out, FrameOutput):
                self.frame_outputs.append(out)

    def show_frame(self, frame: numpy.ndarray):
        for out in self.frame_outputs:
            out.show_frame(frame)

    def close_output(self):
        for out in self.frame_outputs:
            out.close_output()
