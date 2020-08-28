from cv2 import CAP_FIREWIRE
from cv2.cv2 import VideoCapture

from livia.core.input.OpenCVFrameInput import OpenCVFrameInput


class FirewireCamFrameInput(OpenCVFrameInput):
    def __init__(self) -> VideoCapture:
        super().__init(VideoCapture(CAP_FIREWIRE))
