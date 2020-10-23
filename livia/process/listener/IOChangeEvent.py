from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput

if TYPE_CHECKING:
    from livia.process.FrameProcessor import FrameProcessor

T = TypeVar('T', FrameInput, FrameOutput)


class IOChangeEvent(Generic[T]):
    def __init__(self, processor: FrameProcessor, new: T, old: T):
        self.__processor: FrameProcessor = processor
        self.__new: T = new
        self.__old: T = old

    def processor(self) -> FrameProcessor:
        return self.__processor

    def new(self) -> T:
        return self.__new

    def old(self) -> T:
        return self.__old
