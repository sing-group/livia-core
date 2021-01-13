from typing import Callable

from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


def do_nothing_on_show_frame(num_frame: int, frame: ndarray):
    pass


def do_nothing_on_close():
    pass


class CallbackFrameOutput(FrameOutput):
    def __init__(self,
                 output_frame_callback: Callable[[int, ndarray], None] = do_nothing_on_show_frame,
                 close_callback: Callable[[], None] = do_nothing_on_close):
        self._output_frame_callback: Callable[[int, ndarray], None] = output_frame_callback
        self._close_callback: Callable[[], None] = close_callback

    def output_frame(self, num_frame: int, frame: ndarray):
        self._output_frame_callback(num_frame, frame)

    def close(self):
        self._close_callback()
