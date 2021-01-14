from threading import Lock
from typing import Tuple, List

from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


class CompositeFrameOutput(FrameOutput):
    def __init__(self, first_output: FrameOutput, second_output: FrameOutput, *args: FrameOutput):
        super().__init__()

        self.__outputs: List[FrameOutput] = [first_output, second_output, *args]

        self.__lock: Lock = Lock()

    def has_descendant(self, output: FrameOutput) -> bool:
        with self.__lock:
            for child in self.__outputs:
                if child == output:
                    return True
                elif isinstance(child, CompositeFrameOutput):
                    if child.has_descendant(output):
                        return True

            return False

    def remove_output(self, output: FrameOutput) -> bool:
        with self.__lock:
            for i in range(0, len(self.__outputs)):
                if self.__outputs[i] == output:
                    self.__outputs.pop(i)
                    return True
                elif isinstance(output, CompositeFrameOutput):
                    if output.remove_output(output):
                        return True

            return False

    @property
    def outputs(self) -> Tuple[FrameOutput, ...]:
        with self.__lock:
            return tuple(self.__outputs)

    def output_frame(self, num_frame: int, frame: ndarray):
        with self.__lock:
            for output in self.__outputs:
                output.output_frame(num_frame, frame)

    def close(self):
        with self.__lock:
            for output in self.__outputs:
                output.close()
