from typing import Optional


class Classification:
    def __init__(self, class_name: str, score: Optional[float] = None):
        self.__class_name: str = class_name
        self.__score: Optional[float] = score

    @property
    def class_name(self) -> str:
        return self.__class_name

    @property
    def score(self) -> Optional[float]:
        return self.__score
