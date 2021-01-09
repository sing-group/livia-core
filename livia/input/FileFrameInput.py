import time
from typing import Optional, Tuple

from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, CAP_PROP_POS_MSEC
from cv2.cv2 import VideoCapture
from numpy import ndarray

from livia.input.OpenCVFrameInput import OpenCVFrameInput
from livia.input.SeekableFrameInput import SeekableFrameInput


class FileFrameInput(OpenCVFrameInput, SeekableFrameInput):
    def __init__(self, path: str, delay: Optional[float] = None):
        super().__init__(VideoCapture(path))
        self.__delay: float = 1 / 25

        if delay is None:
            try:
                self.__delay = 1 / self._capture.get(CAP_PROP_FPS)
            except AttributeError:
                self.__delay = 1 / 25
        else:
            self.__delay = delay

        self.__last_frame_time: float = 0
        self._length_in_frames: int = self._capture.get(CAP_PROP_FRAME_COUNT)

    def next_frame(self) -> Tuple[Optional[int], Optional[ndarray]]:
        if self._capture.isOpened():
            with self._capture_lock:
                if self._capture.isOpened():
                    ret, frame = self._capture.read()
                    num_frame = self._capture.get(CAP_PROP_POS_FRAMES) - 1
                else:
                    return None, None

            elapsed = time.time() - self.__last_frame_time

            if elapsed < self.__delay:
                time.sleep(self.__delay - elapsed)

            self.__last_frame_time = time.time()

            return num_frame, frame if ret else None
        else:
            return None, None

    def go_to_frame(self, frame: int):
        with self._capture_lock:
            self._capture.set(CAP_PROP_POS_FRAMES, frame)

    def go_to_msec(self, msec: float):
        with self._capture_lock:
            self._capture.get(CAP_PROP_POS_MSEC, msec)

    def get_length_in_frames(self) -> int:
        return self._length_in_frames
