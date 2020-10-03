from typing import Union

from livia.core.input.FrameInput import FrameInput
from livia.core.output.FrameOutput import FrameOutput


class IOChangeEvent:
    def __init__(self, processor, new: Union[FrameInput, FrameOutput],
                 old: Union[FrameInput, FrameOutput]):
        self.__processor = processor
        self.__new = new
        self.__old = old

    def processor(self):
        return self.__processor

    def new(self) -> Union[FrameInput, FrameOutput]:
        return self.__new

    def old(self) -> Union[FrameInput, FrameOutput]:
        return self.__old
