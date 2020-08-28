import cv2
import numpy

from livia.core.output.FrameOutput import FrameOutput


class FileFrameOutput(FrameOutput):
    def __init__(self, path, fps, x, y):
        super().__init__()
        if fps is not None and x is not None and y is not None:
            self.out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'XVID'), fps, (x, y))
        else:
            self.out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640, 480))

    def show_frame(self, frame: numpy.ndarray):
        self.out.write(frame)

    def close_output(self):
        self.out.release()
