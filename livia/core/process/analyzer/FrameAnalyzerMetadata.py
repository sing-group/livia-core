import inspect
from functools import wraps
from typing import Tuple, List, Optional

from livia.core.LiviaPropertyMetadata import LiviaPropertyMetadata
from livia.core.livia_property import del_livia_property_attrs, is_livia_property, get_property_metadata
from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer

DEFAULT_FRAME_ANALYZER_NAME: str = "<No name>"


class FrameAnalyzerMetadata(object):
    def __init__(self, analyzer_class, name: str = DEFAULT_FRAME_ANALYZER_NAME):
        if not issubclass(analyzer_class, FrameAnalyzer):
            raise ValueError(f"Invalid analyzer class: {analyzer_class.__name__}")

        self.__analyzer_class = analyzer_class
        self.__name: str = name
        self.__properties: List[FrameAnalyzerPropertyMetadata] = []

        for name, prop in inspect.getmembers(analyzer_class, lambda m: is_livia_property(m)):
            metadata = get_property_metadata(prop)
            self.__properties.append(FrameAnalyzerPropertyMetadata(prop, name, metadata))
            del_livia_property_attrs(prop)

    @property
    def analyzer_class(self):
        return self.__analyzer_class

    @property
    def name(self) -> str:
        return self.__name

    @property
    def properties(self) -> List[Tuple[str, property]]:
        return self.__properties

    def __str__(self) -> str:
        text = f"{self.analyzer_class}({self.name}): "
        if self.properties:
            for property_meta in self.properties:
                text += f"{property_meta}, "

        return text[:-2]


class FrameAnalyzerPropertyMetadata(object):
    def __init__(self, prop: property, name: str, metadata: LiviaPropertyMetadata):
        self.__property: property = prop
        self.__name: str = name
        self.__descriptive_name: str = metadata.name if metadata.name is not None else name
        self.__order: Optional[int] = metadata.order

    @property
    def prop(self) -> property:
        return self.__property

    @property
    def name(self) -> str:
        return self.__name

    @property
    def descriptive_name(self) -> str:
        return self.__descriptive_name

    @property
    def order(self) -> Optional[int]:
        return self.__order

    def __str__(self):
        return f"{self.name} (name={self.descriptive_name}, order={self.order})"


def frame_analyzer(cls=None, *, name: str = DEFAULT_FRAME_ANALYZER_NAME):
    # This import must be done here to avoid cross import
    from livia.core.process.analyzer.FrameAnalyzerManager import FrameAnalyzerManager

    if cls:
        FrameAnalyzerManager.register_analyzer(FrameAnalyzerMetadata(cls))
        return cls
    else:
        @wraps(cls)
        def wrapper(clazz):
            FrameAnalyzerManager.register_analyzer(FrameAnalyzerMetadata(clazz, name=name))
            return clazz
        return wrapper
