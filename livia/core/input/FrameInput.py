from abc import ABC, abstractmethod

from cv2 import CAP_PROP_FPS
from numpy import ndarray


class FrameInput(ABC):
    def __init__(self):
        self.x_frame = self.y_frame = 0
        self.cap = None

    @abstractmethod
    def next_frame(self) -> ndarray:
        pass

    def close_source(self):
        self.cap.release()

    def get_fps(self) -> int:
        return self.cap.get(CAP_PROP_FPS)

    def get_frame_size(self) -> int:
        return self.x_frame, self.y_frame
