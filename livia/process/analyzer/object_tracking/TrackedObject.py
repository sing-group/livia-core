from collections import deque, Counter
from copy import deepcopy, copy
from enum import Enum
from random import randrange
from typing import Deque, List, Optional, Union, Iterable, Dict, Any, Tuple

from livia.process.analyzer import DEFAULT_WINDOW_SIZE
from livia.process.analyzer.object_detection.DetectedObject import DetectedObject
from livia.process.analyzer.object_tracking.DetectedObjectGroup import DetectedObjectGroup
from livia.process.analyzer.object_tracking.FrameDetectedObjectGroup import FrameDetectedObjectGroup

_NOT_DETECTED_OBJECT_GROUP: DetectedObjectGroup = DetectedObjectGroup()
_NOT_PROCESSED_OBJECT_GROUP: DetectedObjectGroup = DetectedObjectGroup()


class MissingFrameFillingMethod(Enum):
    NOT_DETECTED = 1
    NOT_PROCESSED = 2
    LAST_NOT_DETECTED = 3


class TrackedObject:
    def __init__(self,
                 initial_detection: Union[
                     FrameDetectedObjectGroup,
                     Iterable[FrameDetectedObjectGroup],
                     Tuple[FrameDetectedObjectGroup, Dict[str, Any]],
                     Iterable[Tuple[FrameDetectedObjectGroup, Dict[str, Any]]]
                 ],
                 window_size: int = DEFAULT_WINDOW_SIZE):
        if window_size <= 0:
            raise ValueError("window_size must be a positive number")

        if isinstance(initial_detection, Iterable):
            if len(initial_detection) == 0:
                raise ValueError("At least one object group must be provided")

            detections = [
                deepcopy(detection) if isinstance(detection, tuple) else (detection, {})
                for detection in initial_detection
            ]

            if len(Counter(detection.class_name for detection, metadata in detections)) != 1:
                raise ValueError("Objects must have the same class")
        else:
            detections = [
                deepcopy(initial_detection) if isinstance(initial_detection, tuple) else (initial_detection, {})
            ]

        self.__id: str = "%032x" % randrange(16 ** 32)  # 32 digits hex number
        self.__detection_by_frame: Deque[Tuple[FrameDetectedObjectGroup, Dict[str, Any]]] = \
            deque(detections, window_size)
        self.__class_name: Optional[str] = detections[0][0].class_name
        self.__window_size: int = window_size

    @property
    def id(self) -> str:
        return self.__id

    @property
    def short_id(self) -> str:
        return self.__id[-8:]

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
        return list(detection for detection, _ in self.__detection_by_frame)

    @property
    def frame_consensus(self) -> List[Optional[DetectedObject]]:
        return list(detection.object_group.create_consensus() for detection, _ in self.__detection_by_frame)

    @property
    def last_frame_consensus(self) -> Optional[DetectedObject]:
        return self.__detection_by_frame[-1][0].object_group.create_consensus()

    def __has_detection(
            self, group: Union[FrameDetectedObjectGroup, Tuple[FrameDetectedObjectGroup, Dict[str, Any]]]
    ) -> bool:
        if isinstance(group, tuple):
            group = group[0]

        return group.object_group != _NOT_DETECTED_OBJECT_GROUP \
               and group.object_group != _NOT_PROCESSED_OBJECT_GROUP

    def list_frame_detections(
            self, max_num_frame: Optional[int] = None, max_detections: Optional[int] = None
    ) -> List[FrameDetectedObjectGroup]:
        max_num_frame = max_num_frame if max_num_frame is not None else self.get_last_num_frame()
        max_detections = max_detections if max_detections is not None else self.__window_size

        detections = list(
            detection for detection, _ in self.__detection_by_frame if detection.num_frame <= max_num_frame
        )

        return detections[-max_detections:]

    def list_metadata(self, key: str) -> List[Any]:
        return [metadata.get(key) for _, metadata in self.__detection_by_frame if key in metadata]

    def get_metadata_for(self, detection: FrameDetectedObjectGroup, key: str) -> Optional[Any]:
        metadata = self._find_metadata_for(detection)

        return metadata.get(key)

    def set_metadata_for(self, detection: FrameDetectedObjectGroup, key: str, value: Any) -> None:
        metadata = self._find_metadata_for(detection)

        metadata[key] = value

    def has_metadata_for(self, detection: FrameDetectedObjectGroup, key: str) -> None:
        metadata = self._find_metadata_for(detection)

        return key in metadata

    def remove_metadata_for(self, detection: FrameDetectedObjectGroup, key: str) -> None:
        metadata = self._find_metadata_for(detection)

        del metadata[key]

    def _find_metadata_for(self, detection: FrameDetectedObjectGroup) -> Dict[str, Any]:
        detection_tuple = next(filter(lambda dt: dt[0] == detection, self.__detection_by_frame), None)

        if detection_tuple is None:
            raise ValueError("detection does not belong to this object tracking")
        else:
            return detection_tuple[1]

    def advance_frame(
            self,
            to_num_frame: Optional[int] = None,
            not_detected_filling_method: MissingFrameFillingMethod = MissingFrameFillingMethod.NOT_DETECTED
    ) -> None:
        last_num_frame = self.get_last_num_frame()

        if to_num_frame is None or to_num_frame <= last_num_frame:
            num_frame = last_num_frame + 1 if to_num_frame is None else to_num_frame

            filling_object_group = _NOT_PROCESSED_OBJECT_GROUP \
                if not_detected_filling_method == MissingFrameFillingMethod.NOT_PROCESSED \
                else _NOT_DETECTED_OBJECT_GROUP

            empty_detection = (FrameDetectedObjectGroup(num_frame, filling_object_group), {})
            self.__detection_by_frame.append(empty_detection)
        else:
            filling_object_group = _NOT_DETECTED_OBJECT_GROUP \
                if not_detected_filling_method == MissingFrameFillingMethod.NOT_DETECTED \
                else _NOT_PROCESSED_OBJECT_GROUP

            for num_frame in range(last_num_frame + 1, to_num_frame):
                empty_detection = (FrameDetectedObjectGroup(num_frame, filling_object_group), {})
                self.__detection_by_frame.append(empty_detection)

            filling_object_group = _NOT_PROCESSED_OBJECT_GROUP \
                if not_detected_filling_method == MissingFrameFillingMethod.NOT_PROCESSED \
                else _NOT_DETECTED_OBJECT_GROUP

            empty_detection = (FrameDetectedObjectGroup(to_num_frame, filling_object_group), {})
            self.__detection_by_frame.append(empty_detection)

    def add_frame_detection(self, objects: FrameDetectedObjectGroup, metadata: Dict[str, Any] = {}) -> None:
        if self.__class_name != objects.class_name:
            raise ValueError(
                f"objects class ({objects.class_name}) does not match tracked object class {self.__class_name}")

        last_num_frame = self.get_last_num_frame()
        if last_num_frame < objects.num_frame - 1:
            self.advance_frame(objects.num_frame - 1, MissingFrameFillingMethod.NOT_PROCESSED)

        self.__detection_by_frame.append((objects, deepcopy(metadata)))

    def has_object_detections(self) -> bool:
        return any(detection for detection in self.__detection_by_frame if self.__has_detection(detection))

    def has_detection_in_last_frame(self) -> bool:
        return self.__has_detection(self.__detection_by_frame[-1])

    def get_last_frame_detection(self) -> Optional[FrameDetectedObjectGroup]:
        return self.__detection_by_frame[-1][0] if self.has_detection_in_last_frame() else None

    def get_detection_in_frame(self, num_frame: int) -> Optional[FrameDetectedObjectGroup]:
        detection_tuple = next(filter(lambda dt: dt[0].num_frame == num_frame, self.__detection_by_frame), None)

        return detection_tuple[0] \
            if detection_tuple is not None and self.__has_detection(detection_tuple) \
            else None

    def get_last_num_frame(self) -> int:
        return self.__detection_by_frame[-1][0].num_frame

    def get_last_num_frame_with_detection(self) -> Optional[int]:
        detection = next(filter(lambda d: self.__has_detection(d), reversed(self.__detection_by_frame)), None)

        return None if detection is None else detection[0].num_frame

    def get_first_num_frame(self) -> int:
        return self.__detection_by_frame[0][0].num_frame

    def count_frames(self) -> int:
        return len(self.__detection_by_frame)

    def count_object_detections(self) -> int:
        return len([detection for detection, _ in self.__detection_by_frame if self.__has_detection(detection)])

    def count_frames_without_detection(self) -> int:
        return len([detection for detection, _
                    in self.__detection_by_frame
                    if detection.object_group == _NOT_DETECTED_OBJECT_GROUP])

    def count_frames_not_processed(self) -> int:
        return len([detection for detection, _
                    in self.__detection_by_frame
                    if detection.object_group == _NOT_PROCESSED_OBJECT_GROUP])

    def calculate_window_coverage_percentage(self) -> float:
        return self.count_frames() / self.__window_size

    def calculate_detection_percentage(self) -> float:
        return self.count_object_detections() / self.count_frames()

    def calculate_not_detected_percentage(self) -> float:
        return self.count_frames_without_detection() / self.count_frames()

    def calculate_not_processed_percentage(self) -> float:
        return self.count_frames_not_processed() / self.count_frames()

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

    def __str__(self):
        def to_char(detection, metadata):
            if detection.object_group == _NOT_DETECTED_OBJECT_GROUP:
                return "╳"
            elif detection.object_group == _NOT_PROCESSED_OBJECT_GROUP:
                return "_"
            elif len(metadata) > 0:
                return "█"
            else:
                return "▒"

        objects_str = "".join(to_char(detection, metadata) for detection, metadata in self.__detection_by_frame)

        return f"{self.short_id} {objects_str}"
