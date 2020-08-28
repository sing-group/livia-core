import time

import cv2

from livia.core.input.FrameInput import FrameInput


class FileFrameInput(FrameInput):
    def __init__(self, path):
        super().__init__()
        self.delay = 0.04
        self.cap = cv2.VideoCapture(path)
        ret, frame = self.cap.read()
        if frame is None:
            raise ValueError("Selected input file does not exists: " + path)
        self.y_frame = frame.shape[0]
        self.x_frame = frame.shape[1]

        self.delay = 1 / self.cap.get(cv2.CAP_PROP_FPS)

    def next_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            time.sleep(self.delay)
            if ret is False:
                return None
            else:
                return frame
