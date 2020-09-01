from livia.core.process.analyzer.FrameAnalyzerMetadata import FrameAnalyzerMetadata


class FrameAnalyzerManager:
    __analyzers = []

    @staticmethod
    def register_analyzer(frame_analyzer_metadata: FrameAnalyzerMetadata):
        FrameAnalyzerManager.__analyzers.append(frame_analyzer_metadata)

    @staticmethod
    def list_analyzers() -> [FrameAnalyzerMetadata]:
        return FrameAnalyzerManager.__analyzers.copy()
