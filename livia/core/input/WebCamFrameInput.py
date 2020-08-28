import cv2
from cv2.cv2 import VideoCapture

from livia.core.input.OpenCVFrameInput import OpenCVFrameInput


class WebCamFrameInput(OpenCVFrameInput):
    def __init__(self, webcam_index=0) -> VideoCapture:
        super().__init__(cv2.VideoCapture(webcam_index))
