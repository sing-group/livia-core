from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


class NoFrameOutput(FrameOutput):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not NoFrameOutput.__instance:
            NoFrameOutput.__instance = super().__new__(cls, *args, **kwargs)

        return NoFrameOutput.__instance

    def output_frame(self, num_frame: int, frame: ndarray):
        pass
