import cv2
import numpy

from livia.core.output.FrameOutput import FrameOutput


class WindowFrameOutput(FrameOutput):

    def show_frame(self, frame: numpy.ndarray):
        cv2.imshow('output', frame)
        self.created = True

    def close_output(self):
        # if self.created:
        try:
            if self.created:
                cv2.destroyWindow('output')
        except AttributeError:
            pass
