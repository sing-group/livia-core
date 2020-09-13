__LIVIA_PROPERTY_ATTRIBUTE = "is_livia_property"


def livia_property(func) -> property:
    func.is_livia_property = True

    return property(func)


def del_livia_property_attrs(prop):
    if hasattr(prop, __LIVIA_PROPERTY_ATTRIBUTE):
        del prop.is_livia_property


def is_livia_property(prop):
    return isinstance(prop, property)\
           and prop.fget is not None\
           and hasattr(prop.fget, __LIVIA_PROPERTY_ATTRIBUTE)\
           and prop.fget.is_livia_property
