from numpy import ndarray

from livia.core.process.analyzer.modification.FrameModification import FrameModification


class NoFrameModification(FrameModification):
    def modify(self, num_frame: int, frame: ndarray) -> ndarray:
        return frame
