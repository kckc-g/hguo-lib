

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
        return x is None

    @staticmethod
    def is_not_none(x):
        return x is not None

def map_all(*fns):
    def _fn(*args, **kwargs):
        return tuple(fn(*args, **kwargs) for fn in fns)
    return _fn

def apply_expand(fn):
    def _fn(*args, **kwargs):
        print args,
        print kwargs
        if args and kwargs:
            return ((args, kwargs), fn(*args, **kwargs))
        elif not args and not kwargs:
            return ((), fn(*args, **kwargs))
        elif args and len(args) == 1:
            return (args[0], fn(args[0]))
        return (args or kwargs, fn(*args, **kwargs))
    return _fn

def zip_apply(*fns):
    def _fn(*args):
        return tuple(fn(arg) for fn, arg in zip(fns, args))
    return _fn

def apply(v, fn):
    return fn(v)

def compose(*fns):
    def _fn(*args):
        return reduce(apply, fns[1:], fns[0](*args))
    return _fn

def expand_args(fn):
    def _fn(args):
        return fn(*args)
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

def test_expand_args():
    assert expand_args(str.split)(['as df', 's']) == ['a', ' df']

def test_map_all():
    assert map_all(str.strip, str.split, str.lower, str.upper)('as df') == ('as df', ['as', 'df'], 'as df', 'AS DF')

def test_apply_expand():
    def _fn(*args, **kwargs):
        return 'r'
    assert apply_expand(_fn)(1, 2) == (1, 'r')
    assert apply_expand(_fn)(1, 2) == ((1, 2), 'r')
    assert apply_expand(_fn)(1, 2, 3) == ((1, 2, 3), 'r')
    assert apply_expand(_fn)(1, 2, 3, kwarg=1) == (((1, 2, 3), {'kwarg':1}), 'r')

def test_zip_apply():
    add1 = lambda v:v + 1
    add2 = lambda v:v * 2
    add3 = lambda v:v - 3
    add4 = lambda v:v + 4
    assert zip_apply(add1, add2, add3, add4)(5, 5, 5, 5) == (6, 10, 2, 9)


def test_apply():
    assert apply(' asdf', str.strip) == 'asdf'

def test_compose():
    add1 = lambda v:v + 1
    add2 = lambda v:v * 2
    add3 = lambda v:v - 3
    add4 = lambda v:v + 4

    assert compose(add1, add2, add3, add4)(3) == 9

test_flatten()