import time
from typing import Optional, Tuple

from cv2 import CAP_PROP_FPS
from cv2.cv2 import VideoCapture
from numpy import ndarray

from livia.input.OpenCVFrameInput import OpenCVFrameInput


class FileFrameInput(OpenCVFrameInput):
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

    def next_frame(self) -> Tuple[Optional[int], Optional[ndarray]]:
        if self._capture.isOpened():
            ret, frame = self._capture.read()
            num_frame = self._frame_count
            self._frame_count += 1

            elapsed = time.time() - self.__last_frame_time

            if elapsed < self.__delay:
                time.sleep(self.__delay - elapsed)

            self.__last_frame_time = time.time()

            return num_frame, frame if ret else None
        else:
            return None, None
