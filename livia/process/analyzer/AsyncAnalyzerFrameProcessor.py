import time
from threading import Thread, Lock, Condition

from numpy import ndarray
from typing import Optional, Tuple, List

from livia.benchmarking.TimeLogger import TimeLogger
from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.analyzer.AnalyzerFrameProcessor import AnalyzerFrameProcessor
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification

DEFAULT_MODIFICATION_PERSISTENCE: int = 0
DEFAULT_NUM_THREADS: int = 1


class AsyncAnalyzerFrameProcessor(AnalyzerFrameProcessor):
    def __init__(self,
                 input: FrameInput,
                 output: FrameOutput,
                 frame_analyzer: FrameAnalyzer,
                 modification_persistence: int = DEFAULT_MODIFICATION_PERSISTENCE,
                 num_threads: int = DEFAULT_NUM_THREADS,
                 daemon: bool = True,
                 delay: Optional[float] = None):
        super().__init__(input, output, frame_analyzer, daemon)

        if delay is not None and delay < 0:
            raise ValueError("delay must be None or a non negative float")

        self._analyzer_thread: List[Optional[Thread]] = [None] * num_threads
        self._delay: Optional[float] = delay

        self._modification_persistence: int = modification_persistence

        self._current_frame: Optional[Tuple[Optional[int], Optional[ndarray]]] = None
        self._current_modification: Optional[Tuple[FrameModification, int]] = None

        self._frame_analyzer_lock: Lock = Lock()
        self._current_modification_lock: Lock = Lock()
        self._current_frame_condition: Condition = Condition(lock=Lock())

        self._tl_analyze_frame: TimeLogger = TimeLogger("Analyze Cycle", self.__class__.__name__)

    @AnalyzerFrameProcessor.frame_analyzer.setter
    def frame_analyzer(self, frame_analyzer: FrameAnalyzer):
        if self._frame_analyzer != frame_analyzer:
            with self._frame_analyzer_lock:
                AnalyzerFrameProcessor.frame_analyzer.fset(self, frame_analyzer)

    def _process_frame(self, frame: ndarray):
        # Frame is copied to prevent analyzers from analyzing manipulated frames
        frame_copy = frame.copy()

        with self._current_frame_condition:
            self._current_frame = [self._num_frame, frame_copy]
            self._current_frame_condition.notify()

        if self._delay is not None:
            time.sleep(self._delay)

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
                self._analyzer_thread[i] = Thread(target=self._analyze_frame, daemon=self._daemon,
                                                  name="Asynchronous Analyzer Thread")
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

            with self._tl_analyze_frame:
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
