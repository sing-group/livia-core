from typing import Optional


class LiviaPropertyMetadata:
    def __init__(self, name: Optional[str] = None, order: Optional[int] = None):
        self.__name: Optional[str] = name
        self.__order: Optional[int] = order

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @property
    def order(self) -> Optional[int]:
        return self.__order
