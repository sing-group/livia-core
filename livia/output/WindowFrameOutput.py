from cv2 import imshow, getWindowProperty, destroyWindow, WND_PROP_VISIBLE, cv2
from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


class WindowFrameOutput(FrameOutput):
    def __init__(self, window_name: str = "frame", destroy_on_close: bool = False, delay: int = 1):
        self.__window_name: str = window_name
        self.__destroy_on_close: bool = destroy_on_close
        self.__delay: int = delay

    def output_frame(self, num_frame: int, frame: ndarray):
        imshow(self.__window_name, frame)
        cv2.waitKey(self.__delay)

    def close(self):
        if self.__destroy_on_close:
            if getWindowProperty(self.__window_name, WND_PROP_VISIBLE) >= 1:
                try:
                    destroyWindow(self.__window_name)
                except AttributeError:
                    pass
