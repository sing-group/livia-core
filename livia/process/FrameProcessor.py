from abc import ABC, abstractmethod
from threading import Thread, Condition, Lock
from typing import Optional, Callable

from numpy import ndarray

from livia.input.FrameInput import FrameInput
from livia.output.FrameOutput import FrameOutput
from livia.process.FrameProcessError import FrameProcessError
from livia.process.listener.EventListeners import EventListeners
from livia.process.listener.IOChangeEvent import IOChangeEvent
from livia.process.listener.IOChangeListener import IOChangeListener
from livia.process.listener.ProcessChangeEvent import ProcessChangeEvent
from livia.process.listener.ProcessChangeListener import ProcessChangeListener


class FrameProcessor(ABC):
    def __init__(self, input: FrameInput, output: FrameOutput, daemon: bool = True):
        self._input: FrameInput = input
        self._output: FrameOutput = output
        self._daemon: bool = daemon

        self._num_frame: Optional[int] = None

        self._alive: bool = False
        self._paused: bool = False

        self._io_change_listeners: EventListeners[IOChangeListener] = EventListeners[IOChangeListener]()
        self._process_change_listeners: EventListeners[ProcessChangeListener] = EventListeners[ProcessChangeListener]()

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

            event = IOChangeEvent(self, self._input, old_input)
            self._io_change_listeners.notify(IOChangeListener.input_changed, event)

    @property
    def output(self) -> FrameOutput:
        return self._output

    @output.setter
    def output(self, output: FrameOutput):
        if output != self._output:
            old_output = self._output
            self._output = output

            event = IOChangeEvent(self, self._output, old_output)
            self._io_change_listeners.notify(IOChangeListener.output_changed, event)

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
        with self._input_lock:
            self._input.play()

        while True:
            if not self._check_running_status():
                break

            with self._input_lock:
                self._num_frame, frame = self._input.next_frame()

                if self._num_frame is None or frame is None:
                    break

            if not self._check_running_status():
                break

            self._process_frame(frame)

        with self._running_condition:
            self._alive = False
            self._paused = False
            self._notify_process_change_event(ProcessChangeListener.finished)

    def _process_frame(self, frame: ndarray):
        manipulated_frame = self._manipulate_frame(frame)

        if self._check_running_status():
            self._output_frame(manipulated_frame)

    @abstractmethod
    def _manipulate_frame(self, frame: ndarray) -> ndarray:
        raise NotImplementedError()

    def _check_running_status(self):
        with self._running_condition:
            if self._paused:
                self._running_condition.notify_all()
                self._running_condition.wait()

            if not self._alive:
                self._play_thread = None
                self._alive = False
                return False
            else:
                return True

    def _input_frame(self):
        with self._input_lock:
            self._num_frame, frame = self._input.next_frame()

            self._notify_process_change_event(ProcessChangeListener.frame_inputted)

    def _output_frame(self, frame: ndarray):
        with self._output_lock:
            if self._check_running_status():
                self._output.output_frame(self._num_frame, frame)

                self._notify_process_change_event(ProcessChangeListener.frame_outputted)

    def pause(self):
        with self._running_condition:
            if self._alive and self._play_thread.is_alive():
                self._paused = True

                self._notify_process_change_event(ProcessChangeListener.paused)
            else:
                raise FrameProcessError("Process is not running")

    def resume(self):
        with self._running_condition:
            if self._paused:
                self._paused = False
                self._running_condition.notify()

                self._notify_process_change_event(ProcessChangeListener.resumed)
            else:
                raise FrameProcessError("Process is not paused")

    def start(self):
        with self._running_condition:
            if self._alive:
                raise FrameProcessError("Process is already running")
            else:
                self._num_frame = None
                self._alive = True
                self._play_thread = Thread(target=self._play, daemon=self._daemon, name="Frame Processor Play Thread")
                self._play_thread.start()
                self._on_start()

                self._notify_process_change_event(ProcessChangeListener.started)

    def stop(self):
        with self._running_condition:
            if self._alive:
                self._paused = False
                self._alive = False
                self._running_condition.notify()  # Awake if paused
                self._on_stop()

                self._notify_process_change_event(ProcessChangeListener.stopped)
            else:
                raise FrameProcessError("Process is not running")

    def stop_and_wait(self):
        thread = self._play_thread
        self.stop()
        thread.join()

    def close(self):
        with self._input_lock:
            with self._output_lock:
                self._input.close()
                self._output.close()

    def _on_start(self):
        pass

    def _on_stop(self):
        pass

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

    def _notify_process_change_event(self,
                                     event_method: Callable[[ProcessChangeListener, ProcessChangeEvent], None]):
        event = ProcessChangeEvent(self, self._num_frame)
        self._process_change_listeners.notify(event_method, event)
