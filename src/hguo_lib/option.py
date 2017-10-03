from common import FunctionHelper

class OptionBase(object):
    __slots__ = ()

    def __bool__(self):
        return self.defined

    def __nonzero__(self):
        return self.defined

    def is_defined(self):
        return self.defined

    def is_empty(self):
        return not self.defined

class Some(OptionBase):
    __slots__ = ('_v',)

    defined = True

    def __init__(self, v):
        self._v = v

    def __iter__(self):
        return iter((self._v,))

    def get(self):
        return self._v

    def get_or_else(self, else_value):
        return self._v

class _Nothing(OptionBase):
    EMPTY_ITER = iter(())
    
    defined = False

    def __iter__(self):
        return self.EMPTY_ITER

    def get(self):
        raise Exception("Get on empty option")

    def get_or_else(self, else_value):
        return else_value

NOTHING = _Nothing()
Nothing = NOTHING

def to_option(value=None, defined_func=bool):
    if defined_func(value):
        return Some(value)
    return NOTHING

from functools import wraps

def wrap_option(fn, defined_func=bool):
    @wraps(fn)
    def _fn(*args, **kwargs):
        v = fn(*args, **kwargs)
        return to_option(v, defined_func=defined_func)
    return _fn

def partial_return(fn):
    @wraps(fn)
    def _fn(*args, **kwargs):
        v = fn(*args, **kwargs)
        return to_option(v, defined_func=FunctionHelper.is_not_none)
    return _fn

def test_option():
    o = to_option(1)
    assert isinstance(o, Some)
    assert o.get() == 1
    assert o.get_or_else(2) == 1
    assert o.is_defined()
    assert not o.is_empty()

    o2 = to_option()
    assert o2 is NOTHING
    assert not o2.is_defined()
    assert o2.is_empty()
    assert o2.get_or_else(3) == 3

    assert to_option(2, lambda x:x != 3) is not NOTHING
    assert to_option(3, lambda x:x != 3) is NOTHING


    @wrap_option
    def test_fn(*args):
        return list(args)

    assert test_fn(1, 2) is not NOTHING
    assert test_fn() is NOTHING

    assert test_fn(1, 2).get() == [1,2]
    assert test_fn(1, 2).get_or_else([2]) == [1,2]

    assert test_fn().get_or_else([3]) == [3]

test_option()







