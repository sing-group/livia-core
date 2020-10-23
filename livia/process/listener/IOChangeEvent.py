from typing import TypeVar, Generic

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput

T = TypeVar('T', FrameInput, FrameOutput)


class IOChangeEvent(Generic[T]):
    def __init__(self, processor, new: T, old: T):
        self.__processor = processor
        self.__new: T = new
        self.__old: T = old

    def processor(self):
        return self.__processor

    def new(self) -> T:
        return self.__new

    def old(self) -> T:
        return self.__old
