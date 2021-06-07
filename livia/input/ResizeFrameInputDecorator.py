from typing import Optional, Tuple

from numpy import ndarray, ascontiguousarray

from livia.input.FrameInput import FrameInput
from livia.input.FrameInputDecorator import FrameInputDecorator


class ResizeFrameInputDecorator(FrameInputDecorator):
    def __init__(self, decorated_input: FrameInput,
                 new_size: Tuple[int, int],
                 offset: Optional[Tuple[int, int]] = None):
        super().__init__(decorated_input)

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
