import io
import collections
import unittest
import doctest
import sys

from test import support

from .pickletester_3 import _AbstractPickleTests
from .pickletester_3 import _AbstractPickleModuleTests
from .pickletester_3 import _AbstractPersistentPicklerTests
from .pickletester_3 import _AbstractPicklerUnpicklerObjectTests
from .pickletester_3 import _AbstractDispatchTableTests
from .pickletester_3 import _BigmemPickleTests
from .pickletester_3 import _AbstractBytestrTests
from .pickletester_3 import _AbstractBytesFallbackTests
from .pickletester_3 import _AbstractBytesAsStringTests

from zodbpickle import pickle_3 as pickle

try:
    from zodbpickle import _pickle
except ImportError:
    has_c_implementation = False
else:
    has_c_implementation = True


class PickleTests(_AbstractPickleModuleTests):
    pass


class PyPicklerBase(object):

    pickler = pickle._Pickler
    unpickler = pickle._Unpickler

    def dumps(self, arg, proto=None, **kwds):
        f = io.BytesIO()
        p = self.pickler(f, proto, **kwds)
        p.dump(arg)
        f.seek(0)
        return bytes(f.read())

    def loads(self, buf, **kwds):
        f = io.BytesIO(buf)
        u = self.unpickler(f, **kwds)
        return u.load()

class PyPicklerTests(PyPicklerBase, _AbstractPickleTests):
    pass

class PyPicklerBytestrTests(PyPicklerBase, _AbstractBytestrTests):
    pass

class PyPicklerBytesFallbackTests(PyPicklerBase, _AbstractBytesFallbackTests):
    pass

class PyPicklerBytesAsStringTests(PyPicklerBase, _AbstractBytesAsStringTests):
    pass

class InMemoryPickleTests(_AbstractPickleTests, _BigmemPickleTests):

    pickler = pickle._Pickler
    unpickler = pickle._Unpickler

    def dumps(self, arg, protocol=None):
        return pickle.dumps(arg, protocol)

    def loads(self, buf, **kwds):
        return pickle.loads(buf, **kwds)


class PyPersPicklerTests(_AbstractPersistentPicklerTests):

    pickler = pickle._Pickler
    unpickler = pickle._Unpickler

    def dumps(self, arg, proto=None):
        class PersPickler(self.pickler):
            def persistent_id(subself, obj):
                return self.persistent_id(obj)
        f = io.BytesIO()
        p = PersPickler(f, proto)
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, buf, **kwds):
        class PersUnpickler(self.unpickler):
            def persistent_load(subself, obj):
                return self.persistent_load(obj)
        f = io.BytesIO(buf)
        u = PersUnpickler(f, **kwds)
        return u.load()


class PyPicklerUnpicklerObjectTests(_AbstractPicklerUnpicklerObjectTests):

    pickler_class = pickle._Pickler
    unpickler_class = pickle._Unpickler


if sys.version_info >= (3, 3):
    class PyDispatchTableTests(_AbstractDispatchTableTests):
        pickler_class = pickle._Pickler
        def get_dispatch_table(self):
            return pickle.dispatch_table.copy()


    class PyChainDispatchTableTests(_AbstractDispatchTableTests):
        pickler_class = pickle._Pickler
        def get_dispatch_table(self):
            return collections.ChainMap({}, pickle.dispatch_table)


if has_c_implementation:
    class CPicklerTests(PyPicklerTests):
        pickler = _pickle.Pickler
        unpickler = _pickle.Unpickler

    class CPicklerBytestrTests(PyPicklerBytestrTests):
        pickler = _pickle.Pickler
        unpickler = _pickle.Unpickler

    class CPicklerBytesFallbackTests(PyPicklerBytesFallbackTests):
        pickler = _pickle.Pickler
        unpickler = _pickle.Unpickler

    class CPicklerBytesAsStringTests(PyPicklerBytesAsStringTests):
        pickler = _pickle.Pickler
        unpickler = _pickle.Unpickler

    class CPersPicklerTests(PyPersPicklerTests):
        pickler = _pickle.Pickler
        unpickler = _pickle.Unpickler

    class CDumpPickle_LoadPickle(PyPicklerTests):
        pickler = _pickle.Pickler
        unpickler = pickle._Unpickler

    class DumpPickle_CLoadPickle(PyPicklerTests):
        pickler = pickle._Pickler
        unpickler = _pickle.Unpickler

    class CPicklerUnpicklerObjectTests(_AbstractPicklerUnpicklerObjectTests):
        pickler_class = _pickle.Pickler
        unpickler_class = _pickle.Unpickler

    if sys.version_info >= (3, 3):
        class CDispatchTableTests(_AbstractDispatchTableTests):
            pickler_class = pickle.Pickler
            def get_dispatch_table(self):
                return pickle.dispatch_table.copy()

        class CChainDispatchTableTests(_AbstractDispatchTableTests):
            pickler_class = pickle.Pickler
            def get_dispatch_table(self):
                return collections.ChainMap({}, pickle.dispatch_table)


def choose_tests():
    tests = [PickleTests, PyPicklerTests, PyPersPicklerTests,
             PyPicklerBytestrTests, PyPicklerBytesFallbackTests,
             PyPicklerBytesAsStringTests]
    if sys.version_info >= (3, 3):
        tests.extend([PyDispatchTableTests, PyChainDispatchTableTests])
    if has_c_implementation:
        tests.extend([CPicklerTests, CPersPicklerTests,
                      CPicklerBytestrTests, CPicklerBytesFallbackTests,
                      CPicklerBytesAsStringTests,
                      CDumpPickle_LoadPickle, DumpPickle_CLoadPickle,
                      PyPicklerUnpicklerObjectTests,
                      CPicklerUnpicklerObjectTests,
                      InMemoryPickleTests])
        if sys.version_info >= (3, 3):
            tests.extend([CDispatchTableTests, CChainDispatchTableTests])
    return tests

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(t) for t in choose_tests()
    ] + [
        doctest.DocTestSuite(pickle),
    ])
