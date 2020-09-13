from abc import abstractmethod

from numpy import ndarray

from livia.core.process.analyzer.modification.FrameModification import FrameModification
from livia.core.process.analyzer.modification.NoFrameModification import NoFrameModification


class CompositeFrameModification(FrameModification):
    def __init__(self, child: FrameModification = NoFrameModification()):
        self._child = child

    def modify(self, num_frame: int, frame: ndarray) -> ndarray:
        return self._composite_modify(num_frame, self._child.modify(num_frame, frame))

    @abstractmethod
    def _composite_modify(self, num_frame: int, frame: ndarray) -> ndarray:
        raise NotImplementedError()
