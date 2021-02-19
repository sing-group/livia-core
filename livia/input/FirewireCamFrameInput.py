from cv2 import CAP_FIREWIRE
from cv2 import VideoCapture

from livia.input.OpenCVFrameInput import OpenCVFrameInput


class FirewireCamFrameInput(OpenCVFrameInput):
    def __init__(self):
        super().__init__(VideoCapture(CAP_FIREWIRE))
