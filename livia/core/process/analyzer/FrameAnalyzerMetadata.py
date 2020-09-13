import inspect
from functools import wraps

from livia.core.livia_property import del_livia_property_attrs, is_livia_property
from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer


class FrameAnalyzerMetadata(object):
    def __init__(self, analyzer_class, name: str = "no name"):
        if not issubclass(analyzer_class, FrameAnalyzer):
            raise ValueError(f"Invalid analyzer class: {analyzer_class.__name__}")

        self.__analyzer_class = analyzer_class
        self.__name = name
        self.__properties = inspect.getmembers(analyzer_class, lambda m: is_livia_property(m))

        for name, prop in self.__properties:
            del_livia_property_attrs(prop)

    @property
    def analyzer_class(self):
        return self.__analyzer_class

    @property
    def name(self) -> str:
        return self.__name

    @property
    def properties(self) -> {str, property}:
        return self.__properties


def frame_analyzer(cls=None, *, name: str = "<No name>"):
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
