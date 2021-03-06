# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _example
else:
    import _example

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class StopIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _example.StopIterator_swiginit(self, _example.new_StopIterator())
    __swig_destroy__ = _example.delete_StopIterator

# Register StopIterator in _example:
_example.StopIterator_swigregister(StopIterator)

class Iterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, _cur, _end):
        _example.Iterator_swiginit(self, _example.new_Iterator(_cur, _end))

    def __iter__(self):
        return _example.Iterator___iter__(self)
    cur = property(_example.Iterator_cur_get, _example.Iterator_cur_set)
    end = property(_example.Iterator_end_get, _example.Iterator_end_set)

    def __next__(self):
        return _example.Iterator___next__(self)
    __swig_destroy__ = _example.delete_Iterator

# Register Iterator in _example:
_example.Iterator_swigregister(Iterator)

class Element(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _example.Element_swiginit(self, _example.new_Element())
    __swig_destroy__ = _example.delete_Element

    def get(self):
        return _example.Element_get(self)

    def set(self, var):
        return _example.Element_set(self, var)

# Register Element in _example:
_example.Element_swigregister(Element)

class Collection(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        _example.Collection_swiginit(self, _example.new_Collection())
    __swig_destroy__ = _example.delete_Collection

    def add(self, element):
        return _example.Collection_add(self, element)

    def begin(self, *args):
        return _example.Collection_begin(self, *args)

    def end(self, *args):
        return _example.Collection_end(self, *args)

    def __iter__(self):
        return _example.Collection___iter__(self)

# Register Collection in _example:
_example.Collection_swigregister(Collection)



