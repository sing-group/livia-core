import cv2
import numpy

from livia.core.input.FrameInput import FrameInput


class FirewireCamFrameInput(FrameInput):

    def __init__(self):
        super().__init__()

        # self.cap = cv2.VideoCapture(cv2.CAP_FIREWIRE)
        self.cap = cv2.VideoCapture(cv2.CAP_FIREWIRE)
        print(self.cap.isOpened())
        # while self.cap.read() == (False, None):
        #     pass
        ret, frame = self.cap.read()
        self.y_frame = frame.shape[0]
        self.x_frame = frame.shape[1]

    def next_frame(self) -> numpy.ndarray:
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            return frame
