from typing import Tuple

import cv2
from numpy import ndarray

from livia.process.analyzer.classification import DEFAULT_TEXT_COLOR
from livia.process.analyzer.classification.Classification import Classification
from livia.process.analyzer.modification.CompositeFrameModification import CompositeFrameModification
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification


class ClassificationFrameModification(CompositeFrameModification):
    def __init__(self,
                 classification: Classification,
                 info_color: Tuple[int, int, int] = DEFAULT_TEXT_COLOR,
                 child: FrameModification = NoFrameModification()):
        super().__init__(child)

        self.__classification: Classification = classification
        self.__info_color: Tuple[int, int, int] = info_color

    @property
    def classification(self) -> Classification:
        return self.__classification

    @property
    def info_color(self) -> Tuple[int, int, int]:
        return self.__info_color

    def _composite_modify(self, num_frame: int, frame: ndarray) -> ndarray:
        self._pre_draw(num_frame, frame)

        text = self.classification.class_name

        if self.classification.score is not None:
            text += f" {self.classification.score:.4f}"

        cv2.putText(frame,
                    self.classification.class_name,
                    (0, 0),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.__info_color, 2)

        self._post_draw(num_frame, frame)

        return frame

    def _pre_draw(self, num_frame: int, frame: ndarray):
        pass

    def _post_draw(self, num_frame: int, frame: ndarray):
        pass
