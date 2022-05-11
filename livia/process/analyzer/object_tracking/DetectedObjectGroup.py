from collections import Counter
from statistics import mean
from typing import Optional, List

from livia.process.analyzer.object_detection.DetectedObject import DetectedObject


class DetectedObjectGroup:
    def __init__(self, objects: List[DetectedObject] = []):
        if len(objects) == 0:
            self.__objects: List[DetectedObject] = objects
            self.__class_name: Optional[str] = None
        else:
            if len(Counter(obj.class_name for obj in objects)) != 1:
                raise ValueError("Objects must have the same class")

            self.__objects: List[DetectedObject] = objects
            self.__class_name: str = objects[0].class_name

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
                location = location.create_intersection(self.__objects[i].location)

            return DetectedObject(location, self.class_name, mean_score)

    @property
    def detected_objects(self) -> List[DetectedObject]:
        return self.__objects

    @property
    def class_name(self) -> Optional[str]:
        return self.__class_name
