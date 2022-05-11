from typing import Set, Optional

from livia.process.analyzer.object_tracking.DetectedObjectGroup import DetectedObjectGroup


class FrameDetectedObjectGroups:
    def __init__(self,
                 num_frame: int,
                 groups: Set[DetectedObjectGroup] = set(),
                 class_names: Optional[Set[str]] = None
                 ):
        self.__num_frame: int = num_frame
        self.__groups: Set[DetectedObjectGroup] = groups
        self.__class_names: Set[str] = \
            set(class_names) if class_names is not None else set(group.class_name for group in groups)

    @property
    def num_frame(self) -> int:
        return self.__num_frame

    @property
    def groups(self) -> Set[DetectedObjectGroup]:
        return self.__groups

    @property
    def class_names(self) -> Set[str]:
        return self.__class_names
