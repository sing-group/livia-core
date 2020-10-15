from cv2 import VideoWriter, VideoWriter_fourcc
from numpy import ndarray

from livia.output.FrameOutput import FrameOutput


class FileFrameOutput(FrameOutput):
    def __init__(self, path: str, fps: float = 30.0, width: int = 640, height: int = 480):
        super().__init__()

        fourcc = "mp4v" if "mp4" in path else "XVID"

        self.__output = VideoWriter(path, VideoWriter_fourcc(*fourcc), fps, (width, height))

    def show_frame(self, frame: ndarray):
        self.__output.write(frame)

    def close(self):
        self.__output.release()
