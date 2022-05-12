from copy import deepcopy
from typing import Optional, List

from livia.process.analyzer.object_detection.DetectedObject import DetectedObject
from livia.process.analyzer.object_tracking.DetectedObjectGroup import DetectedObjectGroup


class FrameDetectedObjectGroup:
    def __init__(self, num_frame: int, object_group: DetectedObjectGroup):
        self.__num_frame: int = num_frame
        self.__object_group: DetectedObjectGroup = object_group

    @property
    def num_frame(self) -> int:
        return self.__num_frame

    @property
    def class_name(self) -> Optional[str]:
        return self.__object_group.class_name

    @property
    def detected_objects(self) -> List[DetectedObject]:
        return self.__object_group.detected_objects.copy()

    @property
    def object_group(self) -> DetectedObjectGroup:
        return self.__object_group

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return FrameDetectedObjectGroup(
            self.__num_frame,
            deepcopy(self.__object_group, memodict)
        )
