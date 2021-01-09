from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from livia.process.analyzer.HasThreshold import HasThreshold


class ThresholdChangeEvent:
    def __init__(self, source: HasThreshold, new: float, old: float):
        self.__source: HasThreshold = source
        self.__new: float = new
        self.__old: float = old

    @property
    def source(self) -> HasThreshold:
        return self.__source

    @property
    def new(self) -> float:
        return self.__new

    @property
    def old(self) -> float:
        return self.__old
