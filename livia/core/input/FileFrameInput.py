import time

from cv2 import CAP_PROP_FPS
from cv2.cv2 import VideoCapture
from numpy import ndarray

from livia.core.input.OpenCVFrameInput import OpenCVFrameInput


class FileFrameInput(OpenCVFrameInput):
    def __init__(self, path: str, delay: int = None):
        super().__init__(VideoCapture(path))

        if delay is None:
            try:
                self.__delay = 1 / self._capture.get(CAP_PROP_FPS)
            except AttributeError:
                self.__delay = 0.04
        else:
            self.__delay = delay

        self.__last_frame_time = 0

    def next_frame(self) -> ndarray:
        if self._capture.isOpened():
            ret, frame = self._capture.read()

            elapsed = time.time() - self.__last_frame_time

            if elapsed < self.__delay:
                time.sleep(self.__delay - elapsed)

            self.__last_frame_time = time.time()
            if ret is False:
                return None
            else:
                return frame
