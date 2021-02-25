from threading import Thread, Lock, Condition
from typing import Optional

from numpy import ndarray

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.analyzer.AnalyzerFrameProcessor import AnalyzerFrameProcessor
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.modification.FrameModification import FrameModification


class AsyncAnalyzerFrameProcessor(AnalyzerFrameProcessor):
    def __init__(self, input: FrameInput, output: FrameOutput, frame_analyzer: FrameAnalyzer, daemon: bool = True):
        super().__init__(input, output, frame_analyzer, daemon)
        print("HELLO")

        self._analyzer_thread: Optional[Thread] = None

        self._current_frame: Optional[ndarray] = None
        self._current_num_frame: Optional[int] = None

        self._frame_analyzer_lock: Lock = Lock()
        self._current_modification: Optional[FrameModification] = None
        self._current_modification_lock: Lock = Lock()
        self._modification_condition: Condition = Condition(lock=Lock())

    @AnalyzerFrameProcessor.frame_analyzer.setter
    def frame_analyzer(self, frame_analyzer: FrameAnalyzer):
        if self._frame_analyzer != frame_analyzer:
            with self._frame_analyzer_lock:
                AnalyzerFrameProcessor.frame_analyzer.fset(self, frame_analyzer)

    def _process_frame(self, frame: ndarray):
        with self._modification_condition:
            self._current_frame = frame
            self._current_num_frame = self._num_frame
            self._modification_condition.notify()

        super()._process_frame(frame)

    def _manipulate_frame(self, frame: ndarray) -> ndarray:
        if self._num_frame is None:
            raise RuntimeError("self._num_frame should not be None")

        with self._current_modification_lock:
            modification = self._current_modification
            self._current_modification = None

        return modification.modify(self._num_frame, frame) if modification is not None else frame

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
                        num_frame = self._current_num_frame
                        frame = self._current_frame
                        frame_analyzer = self._frame_analyzer
                else:
                    break

            if self._alive:
                modification = frame_analyzer.analyze(num_frame, frame)
            else:
                break

            if self._alive:
                with self._current_modification_lock:
                    self._current_modification = modification
            else:
                break

        self._analyzer_thread = None
