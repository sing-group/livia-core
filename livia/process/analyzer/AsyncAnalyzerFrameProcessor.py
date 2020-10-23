from threading import Thread, Lock, Condition
from typing import Optional, Tuple

from numpy import ndarray

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.analyzer.AnalyzerFrameProcessor import AnalyzerFrameProcessor
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification


class AsyncAnalyzerFrameProcessor(AnalyzerFrameProcessor):
    def __init__(self, input: FrameInput, output: FrameOutput, frame_analyzer: FrameAnalyzer, daemon: bool = True):
        super().__init__(input, output, frame_analyzer, daemon)

        self._analyzer_thread: Optional[Thread] = None

        self._current_frame: Optional[Tuple[int, ndarray]] = None

        self._frame_analyzer_lock: Lock = Lock()
        self._current_modification: Optional[FrameModification] = None
        self._current_modification_lock: Lock = Lock()
        self._modification_condition: Condition = Condition(lock=Lock())

    @AnalyzerFrameProcessor.frame_analyzer.setter
    def frame_analyzer(self, frame_analyzer: FrameAnalyzer):
        if self._frame_analyzer != frame_analyzer:
            with self._frame_analyzer_lock:
                super().frame_analyzer = frame_analyzer

    def process_frame(self, num_frame: int, frame: ndarray):
        with self._modification_condition:
            self._current_frame = (num_frame, frame)
            self._modification_condition.notify()

        modified_frame = self.manipulate_frame(num_frame, frame)

        with self._output_lock:
            self._output.show_frame(modified_frame)

    def manipulate_frame(self, num_frame: int, frame: ndarray) -> ndarray:
        with self._current_modification_lock:
            modification = self._current_modification
            self._current_modification = None

        return modification.modify(num_frame, frame) if modification is not None else frame

    def _on_start(self):
        self._analyzer_thread = Thread(target=self._analyze_frame, daemon=True, name="Asynchronous Analyzer Thread")
        self._analyzer_thread.start()

    def _on_stop(self):
        with self._modification_condition:
            self._modification_condition.notify()

    def stop_and_join(self):
        thread = self._analyzer_thread
        super().stop_and_wait()
        thread.join()

    def _analyze_frame(self):
        while True:
            with self._modification_condition:
                self._modification_condition.wait()
                if self._alive:
                    with self._frame_analyzer_lock:
                        modification = self._frame_analyzer.analyze(*self._current_frame)
                else:
                    break

            with self._current_modification_lock:
                self._current_modification = modification

        self._analyzer_thread = None
