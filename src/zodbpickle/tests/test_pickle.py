from . import _is_pypy
import sys
import types
import unittest

if _is_pypy:
    function_type = types.FunctionType
elif sys.version_info[0] >= 3:
    function_type = types.BuiltinFunctionType
else:
    function_type = types.FunctionType
del sys
del _is_pypy


class TestImportability(unittest.TestCase):

    def test_Pickler(self):
        from zodbpickle.pickle import Pickler
        self.assertIsInstance(Pickler, object)

    def test_Unpickler(self):
        from zodbpickle.pickle import Unpickler
        self.assertIsInstance(Unpickler, object)

    def test_load(self):
        from zodbpickle.pickle import load
        self.assertIsInstance(load, function_type)

    def test_loads(self):
        from zodbpickle.pickle import loads
        self.assertIsInstance(loads, function_type)

    def test_dump(self):
        from zodbpickle.pickle import dump
        self.assertIsInstance(dump, function_type)

    def test_dumps(self):
        from zodbpickle.pickle import dumps
        self.assertIsInstance(dumps, function_type)


def test_suite():
    import sys
    if sys.version_info[0] >= 3:
        from .pickle_3_tests import test_suite
    else:
        from .pickle_2_tests import test_suite
    return unittest.TestSuite([
        test_suite(),
        unittest.defaultTestLoader.loadTestsFromName(__name__),
    ])
