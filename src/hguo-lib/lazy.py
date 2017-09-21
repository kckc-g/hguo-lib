from functools import wraps

class Lazy(object):
    """An function wrapper that is very lazy ...

    It does NOT evaluate until absoluate necessary (when called)
    It raises error when called for a second time (i.e. this object is single use)
    """
    __slots__ = ('_fn', '_args', '_kwargs')

    def __init__(self, fn, *args, **kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        if self._fn is None:
            raise Exception("Lazy unable to evaluate, either no meaning function is provided or the object has already been called.")
        v = self._fn(*self._args, **self._kwargs)
        self._fn = None
        self._args = None
        self._kwargs = None
        return v


def lazy_evaluation(fn):
    @wraps(fn)
    def _fn(*args, **kwargs):
        return Lazy(fn, *args, **kwargs)
    return _fn

def test_lazy():
    class _ttt:
        def __init__(self):
            self.called = False
        def __call__(self, x, y):
            self.called = True
            return x + y
    
    test1 = _ttt()
    l = Lazy(test1, 1, 3)

    assert not test1.called
    assert l() == 4
    assert test1.called

    try:
        l()
        assert False
    except:
        assert True

    @lazy_evaluation
    def test_fn(x, y, mul=1):
        return (x + y) * mul

    l = test_fn(2, 3)
    assert isinstance(l, Lazy)
    assert l() == 5

    l = test_fn(2, 3, 4)
    assert l() == 20

    try:
        l()
        assert False
    except:
        assert True

test_lazy()