from typing import List, Optional, Set

from numpy import ndarray

from livia.process.analyzer.object_detection.DetectedObject import DetectedObject


class FrameObjectDetection:
    def __init__(self, frame: ndarray, objects: List[DetectedObject], class_names: Optional[Set[str]] = None):
        self.__frame: ndarray = frame
        self.__objects: List[DetectedObject] = list(objects)
        self.__class_names: Optional[Set[str]] = None

        if class_names:
            self.__class_names = set(class_names)
        elif all([obj.has_class_name() for obj in objects]):
            self.__class_names = set([obj.class_name for obj in objects if obj.class_name is not None])
        elif any([obj.has_class_name() for obj in objects]):
            raise ValueError("Objects with and without class can't be combined")

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
    def class_names(self) -> Optional[Set[str]]:
        return set(self.__class_names) if self.__class_names is not None else None

    @property
    def objects(self) -> List[DetectedObject]:
        return self.__objects.copy()

    def has_objects(self) -> bool:
        return len(self.__objects) > 0

    def merge(self, detection: "FrameObjectDetection") -> "FrameObjectDetection":
        if self.__frame != detection.frame:
            raise ValueError("Detection objects must share the same frame")

        self_class_names = set(self.__class_names if self.__class_names is not None else [])
        detection_class_names = set(detection.class_names if detection.class_names is not None else [])
        if self_class_names != detection_class_names:
            raise ValueError("Detection objects must share the same classes")

        return FrameObjectDetection(self.__frame, self.__objects + detection.objects, self.__class_names)
