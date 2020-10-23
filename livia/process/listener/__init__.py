from typing import Type

from livia.process.listener.EventListener import EventListener


def build_listener(listener_class: Type[EventListener], **kwargs):
    listener = listener_class()

    for key, value in kwargs.items():
        if not hasattr(listener, key):
            raise ValueError(f"Invalid listener event: {key}")

        setattr(listener, key, value)

    return listener
