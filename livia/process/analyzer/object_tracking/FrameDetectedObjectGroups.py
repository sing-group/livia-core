from typing import Optional, Iterable, FrozenSet

from livia.process.analyzer.object_tracking.DetectedObjectGroup import DetectedObjectGroup


class FrameDetectedObjectGroups:
    def __init__(self,
                 num_frame: int,
                 groups: Iterable[DetectedObjectGroup] = frozenset(),
                 class_names: Optional[Iterable[str]] = None
                 ):
        self.__num_frame: int = num_frame
        self.__groups: FrozenSet[DetectedObjectGroup] = groups
        self.__class_names: FrozenSet[str] = \
            frozenset(class_names) if class_names is not None else frozenset(group.class_name for group in groups)

    @property
    def num_frame(self) -> int:
        return self.__num_frame

    @property
    def groups(self) -> FrozenSet[DetectedObjectGroup]:
        return self.__groups

    @property
    def class_names(self) -> FrozenSet[str]:
        return self.__class_names

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return FrameDetectedObjectGroups(self.__num_frame, self.__groups, self.__class_names)
