from typing import List, Optional, Set

from numpy import ndarray

from livia.process.analyzer.object_detection.DetectedObject import DetectedObject


class FrameObjectDetection:
    def __init__(self, frame: ndarray, objects: List[DetectedObject], class_names: Optional[Set[str]] = None):
        self.__frame: ndarray = frame
        self.__objects: List[DetectedObject] = list(objects)

        if class_names:
            self.__class_names: Optional[Set[str]] = set(class_names)
        elif all([obj.has_class_name() for obj in objects]):
            self.__class_names: Optional[Set[str]] = set([obj.class_name for obj in objects])
        elif any([obj.has_class_name() for obj in objects]):
            raise ValueError("Objects with and without class can't be combined")
        else:
            self.__class_names: Optional[Set[str]] = None

        if self.__class_names:
            if self.__class_names != set([obj.class_name for obj in objects]):
                cn = self.__class_names
                ocn = set([obj.class_name for obj in objects])
                message = f"Class names ({cn}) do not match the classes in the objects ({ocn})"
                raise ValueError(message)

    @property
    def frame(self) -> ndarray:
        return self.__frame

    @property
    def class_names(self) -> Optional[List[str]]:
        return list(self.__class_names)

    @property
    def objects(self) -> Optional[Set[str]]:
        return None if self.__objects is None else self.__objects.copy()

    def has_objects(self) -> bool:
        return len(self.__objects) > 0

    def merge(self, detection: "FrameObjectDetection") -> "FrameObjectDetection":
        if self.__frame != detection.frame:
            raise ValueError("Detection objects must share the same frame")

        if self.__classes != detection.class_names:
            raise ValueError("Detection objects must share the same classes")

        return FrameObjectDetection(self.__frame, self.__objects + detection.objects, self.__classes)
