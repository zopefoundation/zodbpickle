
import unittest
from pathlib import Path
from zodbpickle import slowpickle as zodb_slowpickle
from zodbpickle import fastpickle as zodb_fastpickle
import pickle
from tempfile import TemporaryDirectory

class TestErrorPickle(unittest.TestCase):

    def test_normal_pickle_none_type(self) -> None:
        with TemporaryDirectory() as tmp_path:
            tmp_path = Path(tmp_path)
            with (tmp_path / 'ex1.pickle').open('wb') as file:
                pickle.dump(type(None), file, protocol=3)

            with (tmp_path / 'ex1.pickle').open('rb') as file:
                ex1b = pickle.load(file)

        assert ex1b is type(None)  # Works fine!

    def test_zodb_fastpickle_none_type(self) -> None:
        with TemporaryDirectory() as tmp_path:
            tmp_path = Path(tmp_path)

            with (tmp_path / 'ex1.pickle').open('wb') as file:
                zodb_fastpickle.dump(type(None), file, protocol=3)
            # Raises Exception:
            # _pickle.PicklingError: Can't pickle <class 'NoneType'>: attribute lookup builtins.NoneType failed


            with (tmp_path / 'ex1.pickle').open('rb') as file:
                ex1b = zodb_fastpickle.load(file)

        assert ex1b is type(None)

    def test_zodb_fastpickle_ellipsis(self) -> None:
        with TemporaryDirectory() as tmp_path:
            tmp_path = Path(tmp_path)

            with (tmp_path / 'ex1.pickle').open('wb') as file:
                zodb_fastpickle.dump(type(...), file, protocol=3)
            # Raises Exception:
            # _pickle.PicklingError: Can't pickle <class 'ellipsis'>: attribute lookup builtins.ellipsis failed


            with (tmp_path / 'ex1.pickle').open('rb') as file:
                ex1b = zodb_fastpickle.load(file)

        assert ex1b is type(None)

    def test_zodb_slowpickle_none_type(self) -> None:
        with TemporaryDirectory() as tmp_path:
            tmp_path = Path(tmp_path)

            with (tmp_path / 'ex1.pickle').open('wb') as file:
                zodb_slowpickle.dump(type(None), file, protocol=3)
            # Above Raises the following Exception normally, but not with the changes in this Pull Request:
            # >           raise PicklingError(
            #               "Can't pickle %r: it's not found as %s.%s" %
            #               (obj, module, name))
            # E           _pickle.PicklingError: Can't pickle <class 'NoneType'>: it's not found as builtins.NoneType

            with (tmp_path / 'ex1.pickle').open('rb') as file:
                ex1b = zodb_slowpickle.load(file)

        assert ex1b is type(None)

    def test_zodb_slowpickle_ellipsis(self) -> None:
        with TemporaryDirectory() as tmp_path:
            tmp_path = Path(tmp_path)

            with (tmp_path / 'ex1.pickle').open('wb') as file:
                zodb_slowpickle.dump(type(...), file, protocol=3)
            # Above Raises the following Exception normally, but not with the changes in this Pull Request:
            # _pickle.PicklingError: Can't pickle <class 'ellipsis'>: it's not found as builtins.ellipsis

            with (tmp_path / 'ex1.pickle').open('rb') as file:
                ex1b = zodb_slowpickle.load(file)

        assert ex1b is type(...)


if __name__ == '__main__':
    unittest.main()