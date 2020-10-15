from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


class CompositeFrameOutput(FrameOutput):
    def __init__(self, first_output: FrameOutput, second_output: FrameOutput, *args: FrameOutput):
        super().__init__()

        self.__outputs = [first_output, second_output, *args]

    def show_frame(self, frame: ndarray):
        for output in self.__outputs:
            output.show_frame(frame)

    def close(self):
        for output in self.__outputs:
            output.close()
