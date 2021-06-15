from typing import Optional, Tuple

from livia.input.ResizingFrameInputDecorator import ResizingFrameInputDecorator
from livia.input.SeekableFrameInput import SeekableFrameInput


class SeekableResizingFrameInputDecorator(ResizingFrameInputDecorator, SeekableFrameInput):
    def __init__(self, decorated_input: SeekableFrameInput,
                 new_size: Tuple[int, int],
                 offset: Optional[Tuple[int, int]] = None):
        super(SeekableResizingFrameInputDecorator, self).__init__(decorated_input, new_size, offset)

    def go_to_frame(self, frame: int):
        self._decorated_input.go_to_frame(frame)

    def go_to_msec(self, msec: float):
        self._decorated_input.go_to_msec(msec)

    def get_length_in_frames(self) -> int:
        return self._decorated_input.get_length_in_frames()

    def get_length_in_msecs(self) -> int:
        return self._decorated_input.get_length_in_msecs()
