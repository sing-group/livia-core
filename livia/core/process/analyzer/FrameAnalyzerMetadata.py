import functools

from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer


class FrameAnalyzerMetadata:
    def __init__(self, analyzer_class, name: str = "no name"):
        if not issubclass(analyzer_class, FrameAnalyzer):
            raise ValueError(f"Invalid analyzer class: {analyzer_class.__name__}")

        functools.update_wrapper(self, analyzer_class)
        self.__analyzer_class = analyzer_class
        self.__name = name

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


def frame_analyzer(cls=None, *, name: str = "no name"):
    if cls:
        return FrameAnalyzerMetadata(cls)
    else:
        @functools.wraps(cls)
        def wrapper(clazz):
            return FrameAnalyzerMetadata(clazz, name=name)

        return wrapper
