from collections import Counter
from copy import deepcopy
from statistics import mean
from typing import Optional, List, Iterable

from livia.process.analyzer.object_detection.DetectedObject import DetectedObject


class DetectedObjectGroup:
    def __init__(self, objects: Iterable[DetectedObject] = []):
        if len(objects) == 0:
            self.__objects: List[DetectedObject] = list(objects)
            self.__class_name: Optional[str] = None
        else:
            if len(Counter(obj.class_name for obj in objects)) != 1:
                raise ValueError("Objects must have the same class")

            self.__objects: List[DetectedObject] = list(objects)
            self.__class_name: str = self.__objects[0].class_name

    @property
    def detected_objects(self) -> List[DetectedObject]:
        return self.__objects.copy()

    @property
    def class_name(self) -> Optional[str]:
        return self.__class_name

    def has_detections(self) -> bool:
        return self.count_detections() > 0

    def count_detections(self) -> int:
        return len(self.__objects)

    def create_consensus(self) -> Optional[DetectedObject]:
        count_objects = len(self.__objects)

        if count_objects == 0:
            return None
        elif count_objects == 1:
            return self.__objects[0]
        else:
            scores = [obj.score for obj in self.__objects if obj.has_score()]
            mean_score = mean(scores) if len(scores) > 0 else None

            location = self.__objects[0].location
            for i in range(1, len(self.__objects)):
                location = location.create_union_rectangle(self.__objects[i].location)

            return DetectedObject(location, self.class_name, mean_score)

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return DetectedObjectGroup(deepcopy(self.__objects, memodict))
