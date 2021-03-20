from threading import Lock
from typing import TypeVar, Generic, List, Callable, Union, Iterator

from livia.process.listener.EventListener import EventListener

T = TypeVar('T', bound=EventListener)
E = TypeVar('E')


class EventListenersIterator(Generic[T]):
    def __init__(self, listeners: List[T]):
        self._listeners: List[T] = listeners
        self._index: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._listeners):
            listener = self._listeners[self._index]
            self._index += 1

            return listener
        else:
            raise StopIteration


class NotificationAction(Generic[T]):
    def __init__(self, iterator: Iterator[T], event_name: str, event: E):
        self._iterator: Iterator[T] = iterator
        self._event_name: str = event_name
        self._event: E = event

    @property
    def iterator(self) -> Iterator[T]:
        return self._iterator

    @property
    def event_name(self) -> str:
        return self._event_name

    @property
    def event(self) -> E:
        return self._event


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

    def notify(self, event_method: Union[str, Callable[[T, E], None]], event: E) -> None:
        event_name = event_method if isinstance(event_method, str) else event_method.__name__

        for listener in self:
            getattr(listener, event_name)(event)
