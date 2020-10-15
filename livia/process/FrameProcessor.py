from abc import ABC, abstractmethod
from threading import Thread, Condition, Lock
from typing import List, Optional

from numpy import ndarray

from livia.input import FrameInput
from livia.output import FrameOutput
from livia.process.FrameProcessError import FrameProcessError
from livia.process.listener import IOChangeEvent
from livia.process.listener import IOChangeListener
from livia.process.listener.ProcessChangeEvent import ProcessChangeEvent
from livia.process.listener.ProcessChangeListener import ProcessChangeListener


class FrameProcessor(ABC):
    def __init__(self, input: FrameInput, output: FrameOutput, daemon: bool = True):
        self._input: FrameInput = input
        self._output: FrameOutput = output
        self._daemon: bool = daemon

        self._num_frame = 0

        self._alive: bool = False
        self._paused: bool = False

        self._io_change_listeners: List[IOChangeListener] = []
        self._process_change_listeners: List[ProcessChangeListener] = []

        self._play_thread: Optional[Thread] = None

        self._running_condition: Condition = Condition(lock=Lock())

        self._input_lock: Lock = Lock()
        self._output_lock: Lock = Lock()

    @property
    def input(self) -> FrameInput:
        with self._input_lock:
            return self._input

    @input.setter
    def input(self, input: FrameInput):
        if input != self._input:
            old_input = self._input
            self._input = input

            for listener in self._io_change_listeners:
                listener.input_changed(IOChangeEvent(self, self._input, old_input))

    @property
    def output(self) -> FrameOutput:
        return self._output

    @output.setter
    def output(self, output: FrameOutput):
        if output != self._output:
            old_output = self._output
            self._output = output

            for listener in self._io_change_listeners:
                listener.output_changed(IOChangeEvent(self, self._output, old_output))

    def is_alive(self) -> bool:
        with self._running_condition:
            return self._alive

    def is_running(self) -> bool:
        with self._running_condition:
            return self._play_thread is not None and self._play_thread.is_alive()

    def is_paused(self) -> bool:
        with self._running_condition:
            return self._paused

    def _play(self):
        while True:
            with self._running_condition:
                if self._paused:
                    self._running_condition.notify_all()
                    self._running_condition.wait()

                if not self._alive:
                    self._play_thread = None
                    self._alive = False
                    break

                with self._input_lock:
                    frame = self._input.next_frame()

                if frame is None:
                    self._play_thread = None
                    self._alive = False
                    break

                num_frame = self._num_frame
                self._num_frame += 1

            self.process_frame(num_frame, frame)

        for listener in self._process_change_listeners:
            listener.finished(ProcessChangeEvent(self, self._num_frame - 1))

    def pause(self):
        with self._running_condition:
            if self._alive and self._play_thread.is_alive():
                self._paused = True

                for listener in self._process_change_listeners:
                    listener.paused(ProcessChangeEvent(self, self._num_frame))
            else:
                raise FrameProcessError("Process is not running")

    def resume(self):
        with self._running_condition:
            if self._paused:
                self._paused = False
                self._running_condition.notify()

                for listener in self._process_change_listeners:
                    listener.resumed(ProcessChangeEvent(self, self._num_frame))
            else:
                raise FrameProcessError("Process is not paused")

    def start(self):
        with self._running_condition:
            if self._alive:
                raise FrameProcessError("Process is already running")
            else:
                self._num_frame = 0
                self._alive = True
                self._play_thread = Thread(target=self._play, daemon=self._daemon, name="Frame Processor Play Thread")
                self._play_thread.start()
                self._on_start()
                for listener in self._process_change_listeners:
                    listener.started(ProcessChangeEvent(self, self._num_frame))

    def _on_start(self):
        pass

    def stop(self):
        with self._running_condition:
            if self._alive:
                self._paused = False
                self._alive = False
                self._running_condition.notify()  # Awake if paused
                self._on_stop()
                for listener in self._process_change_listeners:
                    listener.stopped(ProcessChangeEvent(self, self._num_frame))
            else:
                raise FrameProcessError("Process is not running")

    def _on_stop(self):
        pass

    def stop_and_wait(self):
        thread = self._play_thread
        self.stop()
        thread.join()

    def process_frame(self, num_frame: int, frame: ndarray):
        modified_frame = self.manipulate_frame(num_frame, frame)

        with self._output_lock:
            self._output.show_frame(modified_frame)

    @abstractmethod
    def manipulate_frame(self, num_frame: int, frame: ndarray) -> ndarray:
        raise NotImplementedError()

    def close(self):
        with self._input_lock:
            with self._output_lock:
                self._input.close()
                self._output.close()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add_io_change_listener(self, listener: IOChangeListener):
        self._io_change_listeners.append(listener)

    def remove_io_change_listener(self, listener: IOChangeListener):
        self._io_change_listeners.remove(listener)

    def has_io_change_listener(self, listener: IOChangeListener) -> bool:
        return listener in self._io_change_listeners

    def add_process_change_listener(self, listener: ProcessChangeListener):
        self._process_change_listeners.append(listener)

    def remove_process_change_listener(self, listener: ProcessChangeListener):
        self._process_change_listeners.remove(listener)

    def has_process_change_listener(self, listener: ProcessChangeListener) -> bool:
        return listener in self._process_change_listeners
