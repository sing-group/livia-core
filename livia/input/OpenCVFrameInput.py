from typing import Optional, Tuple

from cv2 import CAP_PROP_FPS
from cv2.cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from numpy import ndarray

from livia.input.FrameInput import FrameInput


class OpenCVFrameInput(FrameInput):
    def __init__(self, capture: VideoCapture):
        super().__init__()
        self._capture = capture

    def next_frame(self) -> Optional[ndarray]:
        if self._capture.isOpened():
            ret, frame = self._capture.read()
            return frame
        else:
            return None

    def get_fps(self) -> int:
        return self._capture.get(CAP_PROP_FPS)

    def get_frame_size(self) -> Tuple[int, int]:
        return int(self._capture.get(CAP_PROP_FRAME_WIDTH)), int(self._capture.get(CAP_PROP_FRAME_HEIGHT))

    def close(self):
        self._capture.release()
