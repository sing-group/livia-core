from copy import deepcopy, copy
from typing import Set, Callable, List, Tuple, Optional, Union, Iterable, FrozenSet

from livia.process.analyzer.object_tracking.DetectedObjectGroup import DetectedObjectGroup
from livia.process.analyzer.object_tracking.FrameDetectedObjectGroup import FrameDetectedObjectGroup
from livia.process.analyzer.object_tracking.TrackedObject import TrackedObject


class TrackedObjects:
    def __init__(self, tracked_objects: Iterable[TrackedObject] = set(), window_size: int = 50):
        self.__tracked_objects: Set[TrackedObject] = set(tracked_objects)
        self.__window_size: int = window_size

    @property
    def tracked_objects(self) -> FrozenSet[TrackedObject]:
        return frozenset(self.__tracked_objects)

    def add(self, tracked_object: TrackedObject) -> None:
        self.__tracked_objects.add(tracked_object)

    def remove(self, tracked_object: TrackedObject) -> None:
        self.__tracked_objects.remove(tracked_object)

    def remove_invalid(self,
                       invalid_condition: Callable[[TrackedObject], bool] = lambda to: not to.has_object_detections()
                       ) -> None:
        self.__tracked_objects = set(to for to in self.__tracked_objects if not invalid_condition(to))

    def add_frame_detections(self,
                             num_frame: int,
                             detections: List[Tuple[DetectedObjectGroup, Optional[TrackedObject]]] = [],
                             remove_invalid: Union[bool, Callable[[TrackedObject], bool]] = True) -> None:

        tracked_objects_to_update = self.__tracked_objects.copy()
        for detection in detections:
            group = detection[0]
            tracked_object = detection[1]

            if tracked_object is None:
                tracked_object = TrackedObject(FrameDetectedObjectGroup(num_frame, group), self.__window_size)
                self.__tracked_objects.add(tracked_object)
            else:
                if tracked_object not in self.__tracked_objects:
                    raise ValueError("tracked object does not belong to this tracked objects")

                tracked_object.add_frame_detection(FrameDetectedObjectGroup(num_frame, group))
                tracked_objects_to_update.remove(tracked_object)

        for tracked_object in tracked_objects_to_update:
            tracked_object.advance_frame()

            if callable(remove_invalid) and remove_invalid(tracked_object):
                self.__tracked_objects.remove(tracked_object)
            elif remove_invalid and not tracked_object.has_object_detections():
                self.__tracked_objects.remove(tracked_object)

    def __copy__(self):
        return TrackedObjects(
            copy(self.__tracked_objects),
            self.__window_size
        )

    def __deepcopy__(self, memodict={}):
        return TrackedObjects(
            deepcopy(self.__tracked_objects),
            self.__window_size
        )
