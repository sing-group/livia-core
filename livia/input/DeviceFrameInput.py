from cv2.cv2 import VideoCapture

from livia.input.OpenCVFrameInput import OpenCVFrameInput


class DeviceFrameInput(OpenCVFrameInput):
    def __init__(self, device_index: int = 0):
        capture = VideoCapture()
        capture.setExceptionMode(True)
        capture.open(device_index)

        super().__init__(capture)
