from cv2.cv2 import VideoCapture

from livia.core.input.OpenCVFrameInput import OpenCVFrameInput


class WebCamFrameInput(OpenCVFrameInput):
    def __init__(self, webcam_index: int = 0) -> VideoCapture:
        super().__init__(VideoCapture(webcam_index))
