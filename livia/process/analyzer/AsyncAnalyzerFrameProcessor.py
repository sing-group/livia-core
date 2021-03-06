import time
from threading import Thread, Lock, Condition
from typing import Optional, Tuple, List

from numpy import ndarray

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.analyzer.AnalyzerFrameProcessor import AnalyzerFrameProcessor
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification


class AsyncAnalyzerFrameProcessor(AnalyzerFrameProcessor):
    def __init__(self, input: FrameInput, output: FrameOutput, frame_analyzer: FrameAnalyzer,
                 modification_persistence: int = 0, num_threads: int = 1, daemon: bool = True):
        super().__init__(input, output, frame_analyzer, daemon)

        self._analyzer_thread: List[Optional[Thread]] = [None] * num_threads

        self._modification_persistence: int = modification_persistence

        self._current_frame: Optional[Tuple[Optional[int], Optional[ndarray]]] = None
        self._current_modification: Optional[Tuple[FrameModification, int]] = None

        self._frame_analyzer_lock: Lock = Lock()
        self._current_modification_lock: Lock = Lock()
        self._current_frame_condition: Condition = Condition(lock=Lock())

    @AnalyzerFrameProcessor.frame_analyzer.setter
    def frame_analyzer(self, frame_analyzer: FrameAnalyzer):
        if self._frame_analyzer != frame_analyzer:
            with self._frame_analyzer_lock:
                AnalyzerFrameProcessor.frame_analyzer.fset(self, frame_analyzer)

    def _process_frame(self, frame: ndarray):
        with self._current_frame_condition:
            self._current_frame = [self._num_frame, frame]
            self._current_frame_condition.notify()

        super()._process_frame(frame)

    def _manipulate_frame(self, frame: ndarray) -> ndarray:
        if self._num_frame is None:
            raise RuntimeError("self._num_frame should not be None")

        with self._current_modification_lock:
            modification = self._current_modification
            if modification is not None:
                if modification[1] == self._modification_persistence:
                    self._current_modification = None
                else:
                    modification[1] += 1

        return modification[0].modify(self._num_frame, frame) if modification is not None else frame

    def _on_start(self):
        if self._analyzer_thread[0] is None:
            for i in range(0, len(self._analyzer_thread)):
                self._analyzer_thread[i] = Thread(target=self._analyze_frame, daemon=self._daemon, name="Asynchronous Analyzer Thread")
                self._analyzer_thread[i].start()

    def _on_stop(self):
        with self._current_frame_condition:
            self._current_frame_condition.notify_all()

    def stop_and_join(self):
        threads = self._analyzer_thread
        super().stop_and_wait()
        for thread in threads:
            thread.join()

    def _analyze_frame(self):
        while True:
            with self._current_frame_condition:
                if self._current_frame is None:
                    self._current_frame_condition.wait()
                frame = self._current_frame
                self._current_frame = None

            with self._frame_analyzer_lock:
                frame_analyzer = self._frame_analyzer

            if self._alive:
                modification = frame_analyzer.analyze(*frame)
            else:
                break

            if self._alive:
                with self._current_modification_lock:
                    self._current_modification = [modification, 0]
            else:
                break

        for i in range(0, len(self._analyzer_thread)):
            self._analyzer_thread[i] = None
