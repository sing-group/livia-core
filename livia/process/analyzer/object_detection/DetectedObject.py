from typing import Optional

from livia.process.analyzer.object_detection.ObjectLocation import ObjectLocation


class DetectedObject:
    def __init__(self, location: ObjectLocation, class_name: Optional[str] = None, score: Optional[float] = None):
        self.__location: ObjectLocation = location
        self.__class_name: Optional[str] = class_name
        self.__score: Optional[float] = score

    @property
    def location(self) -> ObjectLocation:
        return self.__location

    @property
    def class_name(self) -> Optional[str]:
        return self.__class_name

    @property
    def score(self) -> Optional[float]:
        return self.__score

    def has_class_name(self) -> bool:
        return self.class_name is not None

    def has_score(self) -> bool:
        return self.score is not None
