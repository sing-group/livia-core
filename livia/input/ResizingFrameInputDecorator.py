from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

from numpy import ndarray, ascontiguousarray

from livia.input.FrameInput import FrameInput
from livia.input.FrameInputDecorator import FrameInputDecorator
from livia.input.SeekableFrameInput import SeekableFrameInput

if TYPE_CHECKING:
    from livia.input.SeekableResizingFrameInputDecorator import SeekableResizingFrameInputDecorator


class ResizingFrameInputDecorator(FrameInputDecorator):
    @staticmethod
    def decorate(decorated_input: FrameInput, new_size: Tuple[int, int],
                 offset: Optional[Tuple[int, int]] = None) -> "ResizingFrameInputDecorator":
        if isinstance(decorated_input, SeekableFrameInput):
            return SeekableResizingFrameInputDecorator(decorated_input, new_size, offset)
        else:
            return ResizingFrameInputDecorator(decorated_input, new_size, offset)

    def __init__(self, decorated_input: FrameInput,
                 new_size: Tuple[int, int],
                 offset: Optional[Tuple[int, int]] = None):
        super(ResizingFrameInputDecorator, self).__init__(decorated_input)

        self.__size: Tuple[int, int] = new_size
        self.__x_0 = 0 if offset is None else offset[0]
        self.__y_0 = 0 if offset is None else offset[1]
        self.__x_1 = self.__x_0 + self.__size[0]
        self.__y_1 = self.__y_0 + self.__size[1]

    def _manipulate_frame(self, frame: Tuple[Optional[int], Optional[ndarray]]) -> \
            Tuple[Optional[int], Optional[ndarray]]:
        return frame[0], None if frame[1] is None else self.__resize(frame[1])

    def get_frame_size(self) -> Tuple[int, int]:
        return self.__size

    def __resize(self, image: ndarray) -> ndarray:
        resized_image = image[self.__x_0:self.__x_1, self.__y_0:self.__y_1]
        return resized_image if resized_image.flags['C_CONTIGUOUS'] else ascontiguousarray(resized_image)
