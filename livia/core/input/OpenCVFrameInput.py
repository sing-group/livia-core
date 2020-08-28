from cv2 import CAP_PROP_FPS
from cv2.cv2 import VideoCapture
from numpy import ndarray

from livia.core.input.FrameInput import FrameInput


class OpenCVFrameInput(FrameInput):
    def __init__(self, capture: VideoCapture):
        super().__init__()
        self._capture = capture

        ret, frame = self._capture.read()

        if frame is None:
            raise ValueError("Error reading from OpenCV input")

        self._frame_height = frame.shape[0]
        self._frame_width = frame.shape[1]

    def next_frame(self) -> ndarray:
        if self._capture.isOpened():
            ret, frame = self._capture.read()
            return frame

    def get_fps(self) -> int:
        return self._capture.get(CAP_PROP_FPS)

    def get_frame_size(self) -> int:
        return self._frame_width, self._frame_height

    def close(self):
        self._capture.release()
