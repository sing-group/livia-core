from cv2 import imshow, getWindowProperty, destroyWindow, WND_PROP_VISIBLE, cv2
from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


class WindowFrameOutput(FrameOutput):
    def __init__(self, winname: str = "frame", destroy_on_close: bool = False, delay: int = 1):
        self.__winname: str = winname
        self.__destroy_on_close: bool = destroy_on_close
        self.__delay: int = delay

    def show_frame(self, frame: ndarray):
        imshow(self.__winname, frame)
        cv2.waitKey(self.__delay)

    def close(self):
        if self.__destroy_on_close:
            if getWindowProperty(self.__winname, WND_PROP_VISIBLE) >= 1:
                try:
                    destroyWindow(self.__winname)
                except AttributeError:
                    pass
