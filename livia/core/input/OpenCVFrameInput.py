from cv2 import CAP_PROP_FPS
from cv2.cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH
from numpy import ndarray

from livia.core.input.FrameInput import FrameInput


class OpenCVFrameInput(FrameInput):
    def __init__(self, capture: VideoCapture):
        super().__init__()
        self._capture = capture

    def next_frame(self) -> ndarray:
        if self._capture.isOpened():
            ret, frame = self._capture.read()
            return frame

    def get_fps(self) -> int:
        return self._capture.get(CAP_PROP_FPS)

    def get_frame_size(self) -> (int, int):
        return int(self._capture.get(CAP_PROP_FRAME_WIDTH)), int(self._capture.get(CAP_PROP_FRAME_HEIGHT))

    def close(self):
        self._capture.release()
