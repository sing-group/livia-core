from livia.core.LiviaPropertyMetadata import LiviaPropertyMetadata

__LIVIA_METADATA_ATTRIBUTE = "livia_properties_metadata"


def livia_property(func=None, **kwargs):
    if func is None:
        def decorator_livia_property(_func):
            setattr(_func, __LIVIA_METADATA_ATTRIBUTE, LiviaPropertyMetadata(**kwargs))

            return property(_func)

        return decorator_livia_property
    else:
        func.is_livia_property = True
        return property(func)


def get_property_metadata(prop) -> LiviaPropertyMetadata:
    if is_livia_property(prop):
        return getattr(prop.fget, __LIVIA_METADATA_ATTRIBUTE)
    else:
        raise ValueError("prop is not a valid livia_property")


def del_livia_property_attrs(prop):
    if hasattr(prop, __LIVIA_METADATA_ATTRIBUTE):
        delattr(prop, __LIVIA_METADATA_ATTRIBUTE)


def is_livia_property(prop) -> bool:
    return isinstance(prop, property)\
           and prop.fget is not None\
           and hasattr(prop.fget, __LIVIA_METADATA_ATTRIBUTE)
