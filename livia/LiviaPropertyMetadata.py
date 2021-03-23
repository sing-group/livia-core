from typing import Optional, Any, Tuple


class LiviaPropertyMetadata:
    def __init__(self,
                 id: str,
                 prop_type: type,
                 name: Optional[str] = None,
                 order: Optional[int] = None,
                 default_value: Optional[Any] = None,
                 hints: Optional[str] = None,
                 hidden: bool = False):
        if id is None:
            raise ValueError("id can't be None")
        if prop_type is None:
            raise ValueError("prop_type can't be None")

        self.__id: str = id
        self.__prop_type: type = prop_type
        self.__name: Optional[str] = name
        self.__order: Optional[int] = order
        self.__default_value: Optional[Any] = default_value
        self.__hints_str: Optional[str] = hints
        self.__hints: Tuple[str, ...] = tuple(hints.split("|")) if hints is not None else tuple()
        self.__hidden: bool = hidden

    @property
    def id(self) -> str:
        return self.__id

    @property
    def prop_type(self) -> type:
        return self.__prop_type

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
    def hints_str(self) -> Optional[str]:
        return self.__hints_str

    @property
    def hints(self) -> Tuple[str, ...]:
        return self.__hints

    @property
    def hidden(self) -> bool:
        return self.__hidden
