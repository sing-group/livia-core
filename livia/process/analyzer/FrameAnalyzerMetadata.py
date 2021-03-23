import inspect
from functools import wraps
from typing import List, Optional, Type, Any

from livia.LiviaPropertyMetadata import LiviaPropertyMetadata
from livia.livia_property import del_livia_property_attrs, is_livia_property, get_property_metadata
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer

DEFAULT_FRAME_ANALYZER_NAME: str = "<No name>"


class FrameAnalyzerPropertyMetadata(LiviaPropertyMetadata):
    def __init__(self, prop: property, name: str, metadata: LiviaPropertyMetadata):
        super().__init__(
            metadata.id,
            metadata.prop_type,
            metadata.name,
            metadata.order,
            metadata.default_value,
            metadata.hints_str,
            metadata.hidden
        )
        self.__property: property = prop
        self.__descriptive_name: str = metadata.name if metadata.name is not None else name

    @property
    def descriptive_name(self) -> str:
        return self.__descriptive_name

    @property
    def prop(self) -> property:
        return self.__property

    def get_value(self, instance: Any) -> Any:
        return self.__property.fget(instance)

    def set_value(self, instance: Any, value: Any):
        self.__property.fset(instance, value)

    def __str__(self):
        return f"{self.name} (id={self.id}, name={self.descriptive_name}, order={self.order}," \
               f" default_value={str(self.default_value)}, hints={self.hints}, hidden={self.hidden})"


class FrameAnalyzerMetadata(object):
    def __init__(self, analyzer_class: Type[FrameAnalyzer], id: str, name: str = DEFAULT_FRAME_ANALYZER_NAME):
        if not issubclass(analyzer_class, FrameAnalyzer):
            raise ValueError(f"Invalid analyzer class: {analyzer_class.__name__}")
        if id is None:
            raise ValueError("id can't be None")

        self.__analyzer_class: Type[FrameAnalyzer] = analyzer_class
        self.__id: str = id
        self.__name: str = name
        self.__properties: List[FrameAnalyzerPropertyMetadata] = []

        for name, prop in inspect.getmembers(analyzer_class, lambda m: is_livia_property(m)):
            metadata = get_property_metadata(prop)
            self.__properties.append(FrameAnalyzerPropertyMetadata(prop, name, metadata))
            del_livia_property_attrs(prop)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def analyzer_class(self) -> Type[FrameAnalyzer]:
        return self.__analyzer_class

    @property
    def name(self) -> str:
        return self.__name

    @property
    def properties(self) -> List[FrameAnalyzerPropertyMetadata]:
        return self.__properties

    def get_property_by_id(self, prop_id: str) -> Optional[FrameAnalyzerPropertyMetadata]:
        for prop in self.__properties:
            if prop.id == prop_id:
                return prop

        return None

    def __str__(self) -> str:
        analyzer_class = self.analyzer_class
        text = f"{analyzer_class.__module__}.{analyzer_class.__name__}({self.name}): "
        if self.properties:
            for property_meta in self.properties:
                text += f"{property_meta}, "

        return text[:-2]


def frame_analyzer(cls=None, *, id: str, name: str = DEFAULT_FRAME_ANALYZER_NAME):
    # This import must be done here to avoid cross import
    from livia.process.analyzer.FrameAnalyzerManager import FrameAnalyzerManager

    if cls:
        FrameAnalyzerManager.register_analyzer(FrameAnalyzerMetadata(cls, id=id, name=name))
        return cls
    else:
        @wraps(cls)
        def wrapper(clazz):
            FrameAnalyzerManager.register_analyzer(FrameAnalyzerMetadata(clazz, id=id, name=name))
            return clazz

        return wrapper
