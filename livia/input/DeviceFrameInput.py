from cv2 import VideoCapture

from livia.input.OpenCVFrameInput import OpenCVFrameInput
from livia_ui.gui.views.utils.Device import Device


class DeviceFrameInput(OpenCVFrameInput):
    def __init__(self, device: Device):
        capture = VideoCapture()
        capture.setExceptionMode(True)
        capture.open(device.index, device.api)

        super().__init__(capture)
