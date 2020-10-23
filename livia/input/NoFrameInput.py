from typing import Optional, Tuple

from numpy import ndarray

from livia.input.FrameInput import FrameInput


class NoFrameInput(FrameInput):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not NoFrameInput.__instance:
            NoFrameInput.__instance = super().__new__(cls, *args, **kwargs)

        return NoFrameInput.__instance

    def next_frame(self) -> Optional[ndarray]:
        return None

    def get_fps(self) -> int:
        return 0

    def get_frame_size(self) -> Tuple[int, int]:
        return 0, 0
