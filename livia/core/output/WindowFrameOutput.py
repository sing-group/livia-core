from cv2 import imshow, getWindowProperty, destroyWindow, WND_PROP_VISIBLE
from numpy import ndarray

from livia.core.output.FrameOutput import FrameOutput


class WindowFrameOutput(FrameOutput):
    def __init__(self, winname: str = "output", destroy_on_exit: bool = False):
        self.__winname = winname
        self.__destroy_on_exit = destroy_on_exit

    def show_frame(self, frame: ndarray):
        imshow(self.__winname, frame)

    def close(self):
        if self.__destroy_on_exit:
            if getWindowProperty(self.__winname, WND_PROP_VISIBLE) >= 1:
                try:
                    destroyWindow(self.__winname)
                except AttributeError:
                    pass
