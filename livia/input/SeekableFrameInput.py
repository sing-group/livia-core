from abc import abstractmethod

from livia.input.FrameInput import FrameInput


class SeekableFrameInput(FrameInput):
    @abstractmethod
    def go_to_frame(self, frame: int):
        raise NotImplementedError()

    def go_to_msec(self, msec: float):
        self.go_to_frame(round(msec * self.get_fps() * 1000))

    @abstractmethod
    def get_length_in_frames(self) -> int:
        raise NotImplementedError()

    def get_length_in_msecs(self) -> int:
        return round(self.get_length_in_frames() / self.get_fps() * 1000)
