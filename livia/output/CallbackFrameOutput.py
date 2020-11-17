from typing import Callable

from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


def do_nothing_on_show_frame(frame: ndarray):
    pass


def do_nothing_on_close():
    pass


class CallbackFrameOutput(FrameOutput):
    def __init__(self,
                 show_frame_callback: Callable[[ndarray], None] = None,
                 close_callback: Callable[[], None] = None):
        self._show_frame_callback: Callable[[ndarray], None] = \
            show_frame_callback if show_frame_callback is not None else do_nothing_on_show_frame
        self._close_callback: Callable[[], None] = \
            close_callback if close_callback is not None else do_nothing_on_close

    def show_frame(self, frame: ndarray):
        self._show_frame_callback(frame)

    def close(self):
        self._close_callback()
