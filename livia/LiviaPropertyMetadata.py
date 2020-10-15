from typing import Optional


class LiviaPropertyMetadata:
    def __init__(self, id: str, name: Optional[str] = None, order: Optional[int] = None):
        if id is None:
            raise ValueError("id can't be None")

        self.__id: str = id
        self.__name: Optional[str] = name
        self.__order: Optional[int] = order

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @property
    def order(self) -> Optional[int]:
        return self.__order
