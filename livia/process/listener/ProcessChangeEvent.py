from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from livia.process.FrameProcessor import FrameProcessor


class ProcessChangeEvent:
    def __init__(self, processor: FrameProcessor, num_frame: int):
        self.__processor: FrameProcessor = processor
        self.__num_frame: int = num_frame

    def processor(self) -> FrameProcessor:
        return self.__processor

    def num_frame(self) -> int:
        return self.__num_frame
