import logging
import os
import pkgutil
from importlib import import_module
from logging import Logger
from typing import List, Dict, Union, Type, Callable

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
    def get_metadata_by_id(id: str) -> FrameAnalyzerMetadata:
        for analyzer in FrameAnalyzerManager.list_analyzers():
            if analyzer.id == id:
                return analyzer

        raise ValueError(f"No analyzer found for id: {id}")

    @staticmethod
    def get_metadata_for(
            class_instance_or_name: Union[Type[FrameAnalyzer], FrameAnalyzerMetadata, FrameAnalyzer, str]
    ) -> FrameAnalyzerMetadata:
        return FrameAnalyzerManager.__get_metadata_by(
            class_instance_or_name,
            lambda metadata, identifier:
                identifier == metadata.analyzer_class.__module__
                or identifier == metadata.analyzer_class.__qualname__
        )

    @staticmethod
    def get_logger_for(
            class_instance_name_or_analyzer_id: Union[Type[FrameAnalyzer], FrameAnalyzerMetadata, FrameAnalyzer, str]
    ) -> Logger:
        analyzer_metadata = FrameAnalyzerManager.__get_metadata_by(
            class_instance_name_or_analyzer_id,
            lambda metadata, identifier:
                identifier == metadata.analyzer_class.__module__
                or identifier == metadata.analyzer_class.__qualname__
                or identifier == metadata.id
        )

        return logging.getLogger(analyzer_metadata.id)

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

    @staticmethod
    def __get_metadata_by(
            class_instance_or_string: Union[Type[FrameAnalyzer], FrameAnalyzerMetadata, FrameAnalyzer, str],
            string_matcher: Callable[[FrameAnalyzerMetadata, str], bool]
    ) -> FrameAnalyzerMetadata:
        if isinstance(class_instance_or_string, FrameAnalyzerMetadata):
            analyzer_class = class_instance_or_string.analyzer_class
        elif isinstance(class_instance_or_string, FrameAnalyzer):
            analyzer_class = class_instance_or_string.__class__
        else:
            analyzer_class = class_instance_or_string

        if isinstance(analyzer_class, str):
            for analyzer in FrameAnalyzerManager.list_analyzers():
                if string_matcher(analyzer, analyzer_class):
                    return analyzer
        else:
            for analyzer in FrameAnalyzerManager.list_analyzers():
                if analyzer.analyzer_class == analyzer_class:
                    return analyzer

        raise ValueError(f"No analyzer found for {class_instance_or_string}")
