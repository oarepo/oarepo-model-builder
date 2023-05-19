class ClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def class_property(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class CachedClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        cache_name = f"_cache_class_property_{klass.__name__}"
        if hasattr(klass, cache_name):
            return getattr(klass, cache_name)
        ret = self.fget.__get__(obj, klass)()
        setattr(klass, cache_name, ret)
        return ret

    def __delete__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        cache_name = f"_cache_class_property_{klass.__name__}"
        if hasattr(klass, cache_name):
            return delattr(klass, cache_name)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")


def cached_class_property(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return CachedClassPropertyDescriptor(func)
