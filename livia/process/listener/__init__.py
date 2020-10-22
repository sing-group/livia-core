def build_listener(listener_class: type, **kwargs):
    listener = listener_class()

    for key, value in kwargs.items():
        if not hasattr(listener, key):
            raise ValueError(f"Invalid listener event: {key}")

        setattr(listener, key, value)

    return listener
