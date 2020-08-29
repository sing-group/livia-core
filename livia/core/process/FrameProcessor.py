from abc import ABC, abstractmethod

from numpy import ndarray

from livia.core.input.FrameInput import FrameInput
from livia.core.output.FrameOutput import FrameOutput


class FrameProcessor(ABC):
    def __init__(self, input_frame: FrameInput, output_frame: FrameOutput):
        self.output = output_frame
        self.input = input_frame

        self.running = True

    def start(self) -> None:
        frame = self.input.next_frame()
        while frame is not None and self.running:
            self.process_frame(frame)
            frame = self.input.next_frame()
        self.stop()

    def stop(self):
        self.running = False
        self.input.close()
        self.output.close()

    def process_frame(self, frame):
        if frame is not None:
            modified_frame = self.manipulate_frame(frame)
            self.output.show_frame(modified_frame)

    @abstractmethod
    def manipulate_frame(self, frame: ndarray) -> ndarray:
        pass
