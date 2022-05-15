import os
import time
from collections import deque
from statistics import mean
from typing import Optional, Deque, Any

from livia.benchmarking import LIVIA_BENCHMARK_LOGGER
from livia.process.analyzer.FrameAnalyzer import FrameAnalyzer
from livia.process.analyzer.FrameAnalyzerManager import FrameAnalyzerManager


class TimeLogger:
    def __init__(self, message: str, reference_object: Any, window_size=int(os.getenv("BENCHMARK_WINDOW_SIZE", 50))):
        self.__message: str = message
        self.__times: Deque[float] = deque([], maxlen=window_size)
        self.__start: Optional[float] = None
        self.__reference_id: Optional[str] = None

        if isinstance(reference_object, FrameAnalyzer):
            self.__reference_id = FrameAnalyzerManager.get_metadata_for(reference_object).id
        else:
            self.__reference_id = str(reference_object)

    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.__start
        self.__times.append(elapsed)
        mean_time = mean(self.__times)

        if self.__reference_id is not None:
            LIVIA_BENCHMARK_LOGGER.info(f"{self.__reference_id},{self.__message},{mean_time},{elapsed}")
        else:
            LIVIA_BENCHMARK_LOGGER.info(f",{self.__message},{mean_time},{elapsed}")
