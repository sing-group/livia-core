from abc import ABC, abstractmethod

from numpy import ndarray

from livia.core.input.FrameInput import FrameInput
from livia.core.output.FrameOutput import FrameOutput


class FrameProcessor(ABC):
    def __init__(self, frame_input: FrameInput, frame_output: FrameOutput):
        self._frame_output = frame_output
        self._frame_input = frame_input

        self._running = False

    def start(self) -> None:
        self._running = True
        num_frame = 0
        frame = self._frame_input.next_frame()
        while frame is not None and self._running:
            self.process_frame(num_frame, frame)
            frame = self._frame_input.next_frame()
            num_frame += 1
        self.stop()

    def stop(self):
        self._running = False
        self._frame_input.close()
        self._frame_output.close()

    def process_frame(self, num_frame: int, frame: ndarray):
        if frame is not None:
            modified_frame = self.manipulate_frame(num_frame, frame)
            self._frame_output.show_frame(modified_frame)

    @abstractmethod
    def manipulate_frame(self, num_frame: int, frame: ndarray) -> ndarray:
        raise NotImplementedError()
