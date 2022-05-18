from collections import deque, Counter
from copy import deepcopy, copy
from typing import Deque, List, Optional, Union, Iterable

from livia.process.analyzer import DEFAULT_WINDOW_SIZE
from livia.process.analyzer.object_detection.DetectedObject import DetectedObject
from livia.process.analyzer.object_tracking.DetectedObjectGroup import DetectedObjectGroup
from livia.process.analyzer.object_tracking.FrameDetectedObjectGroup import FrameDetectedObjectGroup

_EMPTY_DETECTED_OBJECT_GROUP: DetectedObjectGroup = DetectedObjectGroup()


class TrackedObject:
    def __init__(self,
                 initial_detection: Union[FrameDetectedObjectGroup, Iterable[FrameDetectedObjectGroup]],
                 window_size: int = DEFAULT_WINDOW_SIZE):
        if window_size <= 0:
            raise ValueError("window_size must be a positive number")

        if isinstance(initial_detection, Iterable):
            if len(initial_detection) == 0:
                raise ValueError("At least one object group must be provided")

            if len(Counter(obj.class_name for obj in initial_detection)) != 1:
                raise ValueError("Objects must have the same class")

            detections = initial_detection
            initial_detection = initial_detection[0]
        else:
            detections = [initial_detection]

        self.__detection_by_frame: Deque[FrameDetectedObjectGroup] = deque(detections, window_size)
        self.__class_name: Optional[str] = initial_detection.class_name
        self.__window_size: int = window_size

    @property
    def window_size(self) -> int:
        return self.__window_size

    @window_size.setter
    def window_size(self, window_size: int = DEFAULT_WINDOW_SIZE):
        if self.__window_size != window_size:
            if window_size <= 0:
                raise ValueError("window_size must be a positive number")

            self.__window_size = window_size
            self.__detection_by_frame = deque(self.__detection_by_frame, window_size)

    @property
    def class_name(self) -> Optional[str]:
        return self.__class_name

    @property
    def frame_detections(self) -> List[FrameDetectedObjectGroup]:
        return list(self.__detection_by_frame)

    @property
    def frame_consensus(self) -> List[Optional[DetectedObject]]:
        return [detection.object_group.create_consensus() for detection in self.__detection_by_frame]

    @property
    def last_frame_consensus(self) -> Optional[DetectedObject]:
        return self.__detection_by_frame[-1].object_group.create_consensus()

    def advance_frame(self, to_num_frame: Optional[int] = None) -> None:
        last_num_frame = self.get_last_num_frame()

        if to_num_frame is None:
            self.__detection_by_frame.append(
                FrameDetectedObjectGroup(last_num_frame + 1, _EMPTY_DETECTED_OBJECT_GROUP))
        else:
            if to_num_frame <= last_num_frame:
                raise ValueError(
                    f"to_num_frame ({to_num_frame}) must be greater than last frame ({last_num_frame})")

            for num_frame in range(last_num_frame + 1, to_num_frame + 1):
                self.__detection_by_frame.append(FrameDetectedObjectGroup(num_frame, _EMPTY_DETECTED_OBJECT_GROUP))

    def add_frame_detection(self, objects: FrameDetectedObjectGroup) -> None:
        if self.__class_name != objects.class_name:
            raise ValueError(
                f"objects class ({objects.class_name}) does not match tracked object class {self.__class_name}")

        last_num_frame = self.get_last_num_frame()
        if objects.num_frame <= last_num_frame:
            raise ValueError(
                f"objects frame ({object.num_frame}) must be greater thant the last frame ({last_num_frame})"
            )

        if last_num_frame < objects.num_frame - 1:
            self.advance_frame(objects.num_frame - 1)

        self.__detection_by_frame.append(objects)

    def has_object_detections(self) -> bool:
        return any(detection for detection in self.__detection_by_frame
                   if detection.object_group != _EMPTY_DETECTED_OBJECT_GROUP)

    def has_detection_in_last_frame(self) -> bool:
        return self.__detection_by_frame[-1].object_group != _EMPTY_DETECTED_OBJECT_GROUP

    def get_last_num_frame(self) -> int:
        return self.__detection_by_frame[-1].num_frame

    def get_first_num_frame(self) -> int:
        return self.__detection_by_frame[0].num_frame

    def count_frames(self) -> int:
        return len(self.__detection_by_frame)

    def count_object_detections(self) -> int:
        return len([detection for detection in self.__detection_by_frame if
                    detection.object_group != _EMPTY_DETECTED_OBJECT_GROUP])

    def __copy__(self):
        return TrackedObject(
            copy(self.__detection_by_frame),
            self.__window_size
        )

    def __deepcopy__(self, memodict={}):
        return TrackedObject(
            deepcopy(self.__detection_by_frame, memodict),
            self.__window_size
        )
