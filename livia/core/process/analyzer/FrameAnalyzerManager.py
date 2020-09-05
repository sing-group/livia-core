import os
import pkgutil

from livia.core.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.core.process.analyzer.FrameAnalyzerMetadata import FrameAnalyzerMetadata


class FrameAnalyzerManager:
    __analyzers = []

    @staticmethod
    def register_analyzer(frame_analyzer_metadata: FrameAnalyzerMetadata):
        FrameAnalyzerManager.__analyzers.append(frame_analyzer_metadata)

    @staticmethod
    def list_analyzers() -> [FrameAnalyzerMetadata]:
        return FrameAnalyzerManager.__analyzers.copy()

    @staticmethod
    def get_metadata_for(class_or_object) -> FrameAnalyzerMetadata:
        if isinstance(class_or_object, FrameAnalyzerMetadata):
            analyzer_class = class_or_object.analyzer_class
        elif isinstance(class_or_object, FrameAnalyzer):
            analyzer_class = class_or_object.__class__
        else:
            analyzer_class = class_or_object

        for analyzer in FrameAnalyzerManager.list_analyzers():
            if analyzer.analyzer_class == analyzer_class:
                return analyzer

        raise ValueError(f"No analyzer found for class or object: {class_or_object}")

    @staticmethod
    def load_module(module):
        for module_loader, name, ispkg in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            if not ispkg:
                module_loader.find_module(name).load_module(name)
