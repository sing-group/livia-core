from livia.livia_property import livia_property
from livia.process.analyzer.listener.ThresholdChangeEvent import ThresholdChangeEvent
from livia.process.analyzer.listener.ThresholdChangeListener import ThresholdChangeListener
from livia.process.listener.EventListeners import EventListeners


class HasThreshold:
    def __init__(self,
                 initial_threshold: float = 0.0,
                 min_threshold: float = 0.0,
                 max_threshold: float = 1.0,
                 threshold_step: float = 0.01
                 ):
        self._threshold: float = initial_threshold
        self._min_threshold: float = min_threshold
        self._max_threshold: float = max_threshold
        self._threshold_step: float = threshold_step

        self._threshold_change_listeners: EventListeners[ThresholdChangeListener] = \
            EventListeners[ThresholdChangeListener]()

    @livia_property(id="threshold", name="Threshold", default_value=0.0)
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: float):
        if self._threshold != threshold:
            if threshold < self._min_threshold or threshold > self._max_threshold:
                raise ValueError(
                    f"threshold ({threshold}) must be in range [{self._min_threshold}, {self._max_threshold}]")

            old_threshold = self._threshold
            self._threshold = threshold
            event = ThresholdChangeEvent(self, self._threshold, old_threshold)
            self._threshold_change_listeners.notify(ThresholdChangeListener.threshold_changed, event)

    @property
    def min_threshold(self) -> float:
        return self._min_threshold

    @property
    def max_threshold(self) -> float:
        return self._max_threshold

    @property
    def threshold_step(self) -> float:
        return self._threshold_step

    def increase_threshold(self):
        self.threshold = min(self.threshold + self._threshold_step, self._max_threshold)

    def decrease_threshold(self):
        self.threshold = max(self.threshold - self._threshold_step, self._min_threshold)

    def add_threshold_change_listener(self, listener: ThresholdChangeListener):
        self._threshold_change_listeners.append(listener)

    def remove_threshold_change_listener(self, listener: ThresholdChangeListener):
        self._threshold_change_listeners.remove(listener)

    def has_threshold_change_listener(self, listener: ThresholdChangeListener) -> bool:
        return listener in self._threshold_change_listeners
