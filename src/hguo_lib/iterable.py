from itertools import dropwhile
from itertools import ifilter
from itertools import ifilterfalse
from itertools import imap
from itertools import izip
from itertools import takewhile

from option import partial_return

from common import flatten
from common import FunctionHelper
from common import apply_all

class Materialiser(object):
    def to_list(self):
        return list(iter(self))

    def to_set(self):
        return set(iter(self))

    def to_dict(self):
        return dict(iter(self))

    def to_map(self):
        return self.to_dict()

    def count(self):
        return sum(iter(self.map(lambda x:1)))

    def sum(self):
        return sum(iter(self))

    def sort(self, *args, **kwargs):
        return sorted(self.to_list(), *args, **kwargs)

    def reduce(self, fn, init=None):
        return reduce(fn, self, init)
    fold = reduce
    fold_left = reduce

class Iterable(Materialiser):
    def __init__(self, it):
        self._it = iter(it)

    def __iter__(self):
        return iter(self._it)

    def map(self, *fns):
        if len(fns) == 1:
            self._it = imap(fns[0], self._it)
        elif len(fns) > 1:
            self._it = imap(apply_all(*fns), self._it)
        return self

    def flatten(self):
        self._it = flatten(self._it)
        return self

    def flatmap(self, *fns):
        return self.flatten().map(*fns)

    def partial_map(self, fn):
        return self.map(partial_return(fn))

    def filter(self, predicate=bool):
        self._it = ifilter(predicate, self._it)
        return self

    def filter_not(self, predicate):
        self._it = ifilterfalse(predicate, self._it)
        return self

    def takewhile(self, f):
        self._it = takewhile(f, self._it)
        return self

    def dropwhile(self, f):
        self._it = dropwhile(f, self._it)
        return self

    def zip_with(self, *others):
        self._it = izip(self._it, *others)
        return self

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

class QueueIter:
    def __init__(self):
        self._queue = Queue()

    def __iter__(self):
        return self

    def next(self):
        return self._queue.get()

    

def test_iterable():
    assert Iterable([1,2,3]).map(lambda x: 2*x).map(lambda x:x+1).to_list() == [3, 5, 7]
    assert Iterable([1,2,3]).map(lambda x: 2*x).map(lambda x:x+1).sum() == 15

    assert Iterable([1,2,3]).map(lambda x: 2*x, lambda x:x+1).to_list() == [(2, 2), (4, 3), (6, 4)]

    assert Iterable(xrange(10)).count() == 10

    assert Iterable([3, 1, 4, 2]).sort() == [1,2,3,4]

    assert Iterable([1,2,3,3,4]).to_set() == set([4,3,2,1])

    assert Iterable([1,2,3]).map(FunctionHelper.this, lambda x: 2*x).to_dict() == {2:4, 3:6, 1:2}

    assert Iterable([1,[2],[[3,4],5]]).flatmap(lambda x: x+10).to_list() == [11, 12, 13, 14, 15]

    assert Iterable([1,2,3,4,5,6]).filter(lambda x:x%2 == 0).to_list() == [2,4,6]
    assert Iterable([1,2,3,4,5,6]).filter_not(lambda x:x%2 == 0).to_list() == [1,3,5]

    def testfn(x):
        if x == 1:
            return 5
        if x == 3:
            return 10

    assert Iterable([1,2,3,4]).partial_map(testfn).flatmap().to_list() == [5,10]

    assert Iterable([1,2,3,4]).reduce(lambda accumulated,item:accumulated+item, 100) == 110

    def _acc(accumulated, item):
        accumulated.append(item)
        return accumulated
    assert Iterable([1,2,3,4]).reduce(_acc, []) == Iterable([1,2,3,4]).map(FunctionHelper.this).to_list()

test_iterable()



