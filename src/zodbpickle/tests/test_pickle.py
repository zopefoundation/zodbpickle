import unittest
from cStringIO import StringIO

from .pickletester import _AbstractPickleTests
from .pickletester import _AbstractPickleModuleTests
from .pickletester import _AbstractPersistentPicklerTests
from .pickletester import _AbstractPicklerUnpicklerObjectTests


class PickleTests(_AbstractPickleTests, _AbstractPickleModuleTests):

    def dumps(self, arg, proto=0, fast=0):
        from zodbpickle.pickle import dumps
        # Ignore fast
        return dumps(arg, proto)

    def loads(self, buf):
        from zodbpickle.pickle import loads
        # Ignore fast
        return loads(buf)

    @property
    def module(self):
        from zodbpickle import pickle
        return pickle

    error = KeyError


class PicklerTests(_AbstractPickleTests):

    error = KeyError

    def dumps(self, arg, proto=0, fast=0):
        from zodbpickle.pickle import Pickler
        f = StringIO()
        p = Pickler(f, proto)
        if fast:
            p.fast = fast
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, buf):
        from zodbpickle.pickle import Unpickler
        f = StringIO(buf)
        u = Unpickler(f)
        return u.load()


class PersPicklerTests(_AbstractPersistentPicklerTests):

    def dumps(self, arg, proto=0, fast=0):
        from zodbpickle.pickle import Pickler
        class PersPickler(Pickler):
            def persistent_id(subself, obj):
                return self.persistent_id(obj)
        f = StringIO()
        p = PersPickler(f, proto)
        if fast:
            p.fast = fast
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, buf):
        from zodbpickle.pickle import Unpickler
        class PersUnpickler(Unpickler):
            def persistent_load(subself, obj):
                return self.persistent_load(obj)
        f = StringIO(buf)
        u = PersUnpickler(f)
        return u.load()


class PicklerUnpicklerObjectTests(_AbstractPicklerUnpicklerObjectTests):

    @property
    def pickler_class(self):
        from zodbpickle._pickle import Pickler
        return  Pickler

    @property
    def unpickler_class(self):
        from zodbpickle._pickle import Unpickler
        return  Unpickler


class cPickleBase(object):

    @property
    def error(self):
        from zodbpickle._pickle import BadPickleGet
        return BadPickleGet


class cPickleTests(_AbstractPickleTests,
                   _AbstractPickleModuleTests,
                   cPickleBase,
                  ):
    def setUp(self):
        from zodbpickle._pickle import dumps
        from zodbpickle._pickle import loads
        self.dumps = dumps
        self.loads = loads

    @property
    def module(self):
        from zodbpickle import _pickle
        return _pickle


class cPicklePicklerTests(_AbstractPickleTests, cPickleBase):

    def dumps(self, arg, proto=0):
        from zodbpickle._pickle import Pickler
        f = StringIO()
        p = Pickler(f, proto)
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, buf):
        from zodbpickle._pickle import Unpickler
        f = StringIO(buf)
        p = Unpickler(f)
        return p.load()


class cPickleListPicklerTests(_AbstractPickleTests, cPickleBase):

    def dumps(self, arg, proto=0):
        from zodbpickle._pickle import Pickler
        p = Pickler(proto)
        p.dump(arg)
        return p.getvalue()

    def loads(self, *args):
        from zodbpickle._pickle import Unpickler
        f = StringIO(args[0])
        p = Unpickler(f)
        return p.load()


class cPickleFastPicklerTests(_AbstractPickleTests, cPickleBase):

    def dumps(self, arg, proto=0):
        from zodbpickle._pickle import Pickler
        f = StringIO()
        p = Pickler(f, proto)
        p.fast = 1
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, *args):
        from zodbpickle._pickle import Unpickler
        f = StringIO(args[0])
        p = Unpickler(f)
        return p.load()

    def test_recursive_list(self):
        self.assertRaises(ValueError,
                          _AbstractPickleTests.test_recursive_list,
                          self)

    def test_recursive_tuple(self):
        self.assertRaises(ValueError,
                          _AbstractPickleTests.test_recursive_tuple,
                          self)

    def test_recursive_inst(self):
        self.assertRaises(ValueError,
                          _AbstractPickleTests.test_recursive_inst,
                          self)

    def test_recursive_dict(self):
        self.assertRaises(ValueError,
                          _AbstractPickleTests.test_recursive_dict,
                          self)

    def test_recursive_multi(self):
        self.assertRaises(ValueError,
                          _AbstractPickleTests.test_recursive_multi,
                          self)

    def test_nonrecursive_deep(self):
        # If it's not cyclic, it should pickle OK even if the nesting
        # depth exceeds PY_CPICKLE_FAST_LIMIT.  That happens to be
        # 50 today.  Jack Jansen reported stack overflow on Mac OS 9
        # at 64.
        a = []
        for i in range(60):
            a = [a]
        b = self.loads(self.dumps(a))
        self.assertEqual(a, b)

class cPicklePicklerUnpicklerObjectTests(_AbstractPicklerUnpicklerObjectTests):

    @property
    def pickler_class(self):
        from zodbpickle._pickle import Pickler
        return Pickler

    @property
    def unpickler_class(self):
        from zodbpickle._pickle import Unpickler
        return Unpickler


class Node(object):
    pass


class cPickleDeepRecursive(unittest.TestCase):

    def test_issue2702(self):
        # This should raise a RecursionLimit but in some
        # platforms (FreeBSD, win32) sometimes raises KeyError instead,
        # or just silently terminates the interpreter (=crashes).
        from zodbpickle._pickle import dumps
        nodes = [Node() for i in range(500)]
        for n in nodes:
            n.connections = list(nodes)
            n.connections.remove(n)
        self.assertRaises((AttributeError, RuntimeError), dumps, n)

    def test_issue3179(self):
        # Safe test, because I broke this case when fixing the
        # behaviour for the previous test.
        from zodbpickle._pickle import dumps
        res=[]
        for x in range(1,2000):
            res.append(dict(doc=x, similar=[]))
        dumps(res)


def test_suite():
    import unittest
    return unittest.TestSuite((
        unittest.makeSuite(PickleTests),
        unittest.makeSuite(PicklerTests),
        unittest.makeSuite(PersPicklerTests),
        unittest.makeSuite(PicklerUnpicklerObjectTests),
        unittest.makeSuite(cPickleTests),
        unittest.makeSuite(cPicklePicklerTests),
        unittest.makeSuite(cPickleListPicklerTests),
        unittest.makeSuite(cPickleFastPicklerTests),
        unittest.makeSuite(cPickleDeepRecursive),
        unittest.makeSuite(cPicklePicklerUnpicklerObjectTests),
    ))
