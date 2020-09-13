from numpy import ndarray

from livia.core.process.analyzer.modification.FrameModification import FrameModification


class NoFrameModification(FrameModification):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not NoFrameModification.__instance:
            NoFrameModification.__instance = super().__new__(cls, *args, **kwargs)

        return NoFrameModification.__instance

    def modify(self, num_frame: int, frame: ndarray) -> ndarray:
        return frame
