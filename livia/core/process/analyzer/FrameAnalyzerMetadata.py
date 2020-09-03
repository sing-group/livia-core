import functools
import inspect

from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer


class FrameAnalyzerMetadata:
    def __init__(self, analyzer_class, name: str = "no name"):
        if not issubclass(analyzer_class, FrameAnalyzer):
            raise ValueError(f"Invalid analyzer class: {analyzer_class.__name__}")

        functools.update_wrapper(self, analyzer_class)
        self.__analyzer_class = analyzer_class
        self.__name = name

        self.__properties = inspect.getmembers(
            analyzer_class,
            lambda m: isinstance(m, property)
                      and m.fget is not None
                      and hasattr(m.fget, "is_frame_analyzer_property")
                      and m.fget.is_frame_analyzer_property)

        for name, prop in self.__properties:
            del prop.fget.is_frame_analyzer_property

        # This import must be done here to avoid cross import
        from livia.core.process.analyzer.FrameAnalyzerManager import FrameAnalyzerManager
        FrameAnalyzerManager.register_analyzer(self)

    def __call__(self, *args, **kwargs):
        return self.__analyzer_class(*args, **kwargs)

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
    if cls:
        return FrameAnalyzerMetadata(cls)
    else:
        @functools.wraps(cls)
        def wrapper(clazz):
            return FrameAnalyzerMetadata(clazz, name=name)

        return wrapper


def frame_analyzer_property(func):
    func.is_frame_analyzer_property = True

    return property(func)

