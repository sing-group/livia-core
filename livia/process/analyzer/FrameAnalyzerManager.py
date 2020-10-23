import os
import pkgutil
from importlib import import_module
from typing import List, Dict

from livia import LIVIA_LOGGER
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.FrameAnalyzerMetadata import FrameAnalyzerMetadata


class FrameAnalyzerManager:
    __analyzers: List[FrameAnalyzerMetadata] = []

    @staticmethod
    def register_analyzer(frame_analyzer_metadata: FrameAnalyzerMetadata):
        LIVIA_LOGGER.debug(f"Registering frame analyzer metadata: {frame_analyzer_metadata}")
        FrameAnalyzerManager.__analyzers.append(frame_analyzer_metadata)

    @staticmethod
    def list_analyzers() -> List[FrameAnalyzerMetadata]:
        return FrameAnalyzerManager.__analyzers.copy()

    @staticmethod
    def get_metadata_for(class_instance_or_name) -> FrameAnalyzerMetadata:
        if isinstance(class_instance_or_name, FrameAnalyzerMetadata):
            analyzer_class = class_instance_or_name.analyzer_class
        elif isinstance(class_instance_or_name, FrameAnalyzer):
            analyzer_class = class_instance_or_name.__class__
        else:
            analyzer_class = class_instance_or_name

        if isinstance(analyzer_class, str):
            for analyzer in FrameAnalyzerManager.list_analyzers():
                if analyzer_class == analyzer.analyzer_class.__module__ \
                    or analyzer.analyzer_class.__qualname__ == analyzer_class:
                    return analyzer
        else:
            for analyzer in FrameAnalyzerManager.list_analyzers():
                if analyzer.analyzer_class == analyzer_class:
                    return analyzer

        raise ValueError(f"No analyzer found for class or object: {class_instance_or_name}")

    @staticmethod
    def load_module(module):
        for module_loader, name, is_package in pkgutil.iter_modules([os.path.dirname(module.__file__)]):
            if not is_package:
                import_module(f"{module.__name__}.{name}")

    @staticmethod
    def build_analyzer(args: Dict[str, str]) -> FrameAnalyzer:
        metadata = FrameAnalyzerManager.get_metadata_for(args["analyzer"])

        analyzer_class = metadata.analyzer_class
        analyzer = analyzer_class()

        for prop in metadata.properties:
            if prop.name in args:
                setattr(analyzer, prop.name, args[prop.name])

        return analyzer
