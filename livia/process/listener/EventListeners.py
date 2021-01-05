from threading import Lock
from typing import TypeVar, Generic, List

from livia.process.listener.EventListener import EventListener

T = TypeVar('T', bound=EventListener)


class EventListenersIterator(Generic[T]):
    def __init__(self, listeners: List[T]):
        self._listeners: List[T] = listeners
        self._index: int = 0

    def __next__(self):
        if self._index < len(self._listeners):
            listener = self._listeners[self._index]
            self._index += 1

            return listener
        else:
            raise StopIteration


class EventListeners(Generic[T]):
    def __init__(self):
        self._listeners: List[T] = []
        self._lock: Lock = Lock()

    def append(self, listener: T) -> bool:
        with self._lock:
            if listener not in self._listeners:
                self._listeners.append(listener)
                return True
            else:
                return False

    def remove(self, listener: T):
        with self._lock:
            self._listeners.remove(listener)

    def clear(self):
        with self._lock:
            self._listeners.clear()

    def __contains__(self, listener: T) -> bool:
        with self._lock:
            return listener in self._listeners

    def __iter__(self) -> EventListenersIterator[T]:
        with self._lock:
            return EventListenersIterator(self._listeners.copy())
