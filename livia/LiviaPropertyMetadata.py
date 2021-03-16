from typing import Optional, Any


class LiviaPropertyMetadata:
    def __init__(self, id: str, name: Optional[str] = None, order: Optional[int] = None,
                 default_value: Optional[Any] = None, hints: Optional[str] = None,
                 hidden: Optional[bool] = False):
        if id is None:
            raise ValueError("id can't be None")

        self.__id: str = id
        self.__name: Optional[str] = name
        self.__order: Optional[int] = order
        self.__default_value: Optional[Any] = default_value
        self.__hints: Optional[str] = hints
        self.__hidden: Optional[bool] = hidden

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @property
    def order(self) -> Optional[int]:
        return self.__order

    @property
    def default_value(self) -> Optional[Any]:
        return self.__default_value

    @property
    def hints(self) -> Optional[str]:
        return self.__hints

    @property
    def hidden(self) -> Optional[bool]:
        return self.__hidden
