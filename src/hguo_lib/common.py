class FunctionHelper:
    @staticmethod
    def this(x):
        return x

    @staticmethod
    def eq(x):
        return lambda y: y == x

    @staticmethod
    def not_(x):
        return lambda y: y != x

    @staticmethod
    def is_(x):
        return lambda y: y is x

    @staticmethod
    def always_true(x):
        return True

    @staticmethod
    def always_false(x):
        return False

    @staticmethod
    def is_none(x):
        return FunctionHelper.is_(None)

    @staticmethod
    def is_not_none(x):
        return FunctionHelper.not_(None)

def map_to_tuple(keyfunc=None, valuefunc=FunctionHelper.this):
    """Maps inputs to a tuple of two.
    This is handy to turn a stream of tuples to into a dict

    keyfunc and valuefunc are callable with signature: "def f(*args, **kwargs)"

    :param keyfunc: Callable that transforms inputs into a key (first value in tuple)
        Optional, if None, the key is just the inputs (i.e. FunctionHelper.this would be called)
    :param valuefnc: Callable that transforms inputs into a value (second value in tuple)
    """
    keyfunc = keyfunc or FunctionHelper.this
    def _fn(*args, **kwargs):
        return (keyfunc(*args, **kwargs), valuefunc(*args, **kwargs))
    return _fn 

def apply(v, fn):
    return fn(v)

def apply_all(*fns):
    def _fn(*args, **kwargs):
        return tuple(fn(*args, **kwargs) for fn in fns)
    return _fn

def compose(*fns):
    assert fns, 'Compose requires at least one function, none provided'
    def _fn(*args):
        return reduce(apply, fns[1:], fns[0](*args))
    return _fn

def apply_expand_args(fn):
    def _fn(args):
        return fn(*args)
    return _fn

def apply_expand_kwargs(fn):
    def _fn(args):
        return fn(**kwargs)
    return _fn

def flatten(ll):
    if hasattr(ll, '__iter__'):
        for y in ll:
            for x in flatten(y):
                yield x
    else:
        yield ll            


############## TEST FUNCTIONS ###################



def test_flatten():
    assert list(flatten([1])) == [1]
    assert list(flatten([1,[2]])) == [1, 2]
    assert list(flatten([1,[2, 3], 4])) == [1, 2, 3, 4]
    assert list(flatten([5,[6], [[7,8],9], [10]])) == [5, 6, 7, 8, 9, 10]
    assert list(flatten(5)) == [5]
    assert list(flatten('asdf')) == ['asdf']

def test_apply_expand_args():
    assert apply_expand_args(str.split)(['as df', 's']) == ['a', ' df']

def test_apply_all():
    assert apply_all(str.strip, str.split, str.lower, str.upper)('as df') == ('as df', ['as', 'df'], 'as df', 'AS DF')

def test_apply():
    assert apply(' asdf', str.strip) == 'asdf'

def test_compose():
    add1 = lambda v:v + 1
    add2 = lambda v:v * 2
    add3 = lambda v:v - 3
    add4 = lambda v:v + 4

    assert compose(add1, add2, add3, add4)(3) == 9

test_flatten()
