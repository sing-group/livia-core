from typing import Optional

from numpy import ndarray

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.FrameProcessor import FrameProcessor
from livia.process.analyzer.AreaOfInterest import AreaOfInterest
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.listener.FrameAnalyzerChangeEvent import FrameAnalyzerChangeEvent
from livia.process.analyzer.listener.FrameAnalyzerChangeListener import FrameAnalyzerChangeListener
from livia.process.analyzer.modification.FrameModification import FrameModification
from livia.process.analyzer.modification.NoFrameModification import NoFrameModification
from livia.process.listener.EventListeners import EventListeners

DEFAULT_FRAME_RATIO: int = 1


class AnalyzerFrameProcessor(FrameProcessor):
    def __init__(self,
                 input: FrameInput,
                 output: FrameOutput,
                 frame_analyzer: FrameAnalyzer,
                 area_of_interest: Optional[AreaOfInterest] = None,
                 frame_ratio: int = DEFAULT_FRAME_RATIO,
                 daemon: bool = True):
        super().__init__(input, output, daemon)

        self.__current_modification: FrameModification = NoFrameModification()
        self._area_of_interest: Optional[AreaOfInterest] = area_of_interest
        self._frame_ratio: int = frame_ratio

        self._frame_analyzer: FrameAnalyzer = frame_analyzer
        self._frame_analyzer_change_listeners: EventListeners[FrameAnalyzerChangeListener] =\
            EventListeners[FrameAnalyzerChangeListener]()

    def _has_area_of_interest(self) -> bool:
        return self._area_of_interest is not None

    def _manipulate_frame(self, frame: ndarray) -> ndarray:
        if self._num_frame is None:
            raise RuntimeError("self._num_frame should not be None")

        if self._num_frame % self._frame_ratio == 0:
            if self._has_area_of_interest():
                frame_aoi = self._area_of_interest.extract_from(frame)

                modification = self._frame_analyzer.analyze(self._num_frame // self._frame_ratio, frame_aoi.copy())
                self.__current_modification = modification

                modified_frame_aoi = modification.modify(self._num_frame // self._frame_ratio, frame_aoi)

                return self._area_of_interest.replace_on(frame, modified_frame_aoi)
            else:
                modification = self._frame_analyzer.analyze(self._num_frame // self._frame_ratio, frame.copy())
                self.__current_modification = modification

                return modification.modify(self._num_frame // self._frame_ratio, frame)
        else:
            if self._has_area_of_interest():
                frame_aoi = self._area_of_interest.extract_from(frame)

                modification = self.__current_modification

                modified_frame_aoi = modification.modify(self._num_frame // self._frame_ratio, frame_aoi)

                return self._area_of_interest.replace_on(frame, modified_frame_aoi)
            else:
                modification = self.__current_modification

                return modification.modify(self._num_frame // self._frame_ratio, frame)

    @property
    def frame_analyzer(self) -> FrameAnalyzer:
        return self._frame_analyzer

    @frame_analyzer.setter
    def frame_analyzer(self, frame_analyzer: FrameAnalyzer):
        if self._frame_analyzer != frame_analyzer:
            old_frame_analyzer = self._frame_analyzer
            self._frame_analyzer = frame_analyzer

            event = FrameAnalyzerChangeEvent(self, self._frame_analyzer, old_frame_analyzer)
            self._frame_analyzer_change_listeners.notify(FrameAnalyzerChangeListener.analyzer_changed, event)

    def add_frame_analyzer_change_listener(self, listener: FrameAnalyzerChangeListener):
        self._frame_analyzer_change_listeners.append(listener)

    def remove_frame_analyzer_change_listener(self, listener: FrameAnalyzerChangeListener):
        self._frame_analyzer_change_listeners.remove(listener)

    def has_frame_analyzer_change_listener(self, listener: FrameAnalyzerChangeListener) -> bool:
        return listener in self._frame_analyzer_change_listeners
