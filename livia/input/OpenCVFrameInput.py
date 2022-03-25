from threading import Lock
from typing import Optional, Tuple

from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, CAP_PROP_POS_FRAMES, \
    CAP_PROP_POS_MSEC
from numpy import ndarray

from livia.input.FrameInput import FrameInput


class OpenCVFrameInput(FrameInput):
    def __init__(self, capture: VideoCapture):
        super().__init__()
        self._capture: VideoCapture = capture
        self._capture_lock: Lock = Lock()

        self._current_frame: Optional[ndarray] = None

    def next_frame(self) -> Tuple[Optional[int], Optional[ndarray]]:
        if self._capture.isOpened():
            with self._capture_lock:
                if self._capture.isOpened():
                    num_frame = int(self._capture.get(CAP_PROP_POS_FRAMES))
                    ret, self._current_frame = self._capture.read()
                else:
                    ret = False
            if ret:
                return num_frame, self._current_frame

        self._current_frame = None
        return None, None

    def get_current_frame(self) -> Optional[ndarray]:
        return self._current_frame

    def get_current_frame_index(self) -> Optional[int]:
        with self._capture_lock:
            return int(self._capture.get(CAP_PROP_POS_FRAMES)) - 1

    def get_current_msec(self) -> Optional[int]:
        with self._capture_lock:
            return int(self._capture.get(CAP_PROP_POS_MSEC))

    def get_fps(self) -> int:
        with self._capture_lock:
            return self._capture.get(CAP_PROP_FPS)

    def get_frame_size(self) -> Tuple[int, int]:
        with self._capture_lock:
            return int(self._capture.get(CAP_PROP_FRAME_WIDTH)), int(self._capture.get(CAP_PROP_FRAME_HEIGHT))

    def close(self):
        with self._capture_lock:
            self._capture.release()
