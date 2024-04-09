===========
 Changelog
===========

3.3 (unreleased)
================

- Build Windows wheels on GHA.

- Add preliminary support for Python 3.13 as of 3.13a5.


3.2 (2024-02-16)
================

- Add preliminary support for Python 3.13 as of 3.13a3.


3.1 (2023-10-05)
================

- Add support for Python 3.12.


3.0.1 (2023-03-28)
==================

- Fix ``NameError`` in ``.fastpickle`` and ``.slowpickle``.


3.0 (2023-03-24)
================

- Build Linux binary wheels for Python 3.11.

- Add preliminary support for Python 3.12a5.

- Drop support for Python 2.7, 3.5, 3.6.

- Drop support for deprecated ``python setup.py test``.


2.6 (2022-11-17)
================

- Add support for building arm64 wheels on macOS.


2.5 (2022-11-03)
================

- Add support for the final Python 3.11 release.


2.4 (2022-09-15)
================

- Add support for Python 3.11 (as of 3.11.0b3).

- Disable unsafe math optimizations in C code.  See `pull request 73
  <https://github.com/zopefoundation/zodbpickle/pull/73>`_.


2.3 (2022-04-22)
================

- Add support for Python 3.11 (as of 3.11.0a7).


2.2.0 (2021-09-29)
==================

- Add support for Python 3.10.


2.1.0 (2021-09-24)
==================

- Add support for Python 3.9.


2.0.0 (2019-11-13)
==================

- CPython 2: Make ``zodbpickle.binary`` objects smaller and untracked
  by the garbage collector. Now they behave more like the native bytes
  object. Just like it, and just like on Python 3, they cannot have
  arbitrary attributes or be weakly referenced. See `issue 53
  <https://github.com/zopefoundation/zodbpickle/issues/53>`_.

1.1 (2019-11-09)
================

- Add support for Python 3.8.

- Drop support for Python 3.4.


1.0.4 (2019-06-12)
==================

- Fix pickle corruption under certain conditions. See `pull request 47
  <https://github.com/zopefoundation/zodbpickle/pull/47>`_.


1.0.3 (2018-12-18)
==================

- Fix a bug: zodbpickle.slowpickle assigned `_Pickler` to `Unpickler`.


1.0.2 (2018-08-10)
==================

- Add support for Python 3.7.


1.0.1 (2018-05-16)
==================

- Fix a memory leak in pickle protocol 3 under Python 2. See `issue 36
  <https://github.com/zopefoundation/zodbpickle/issues/36>`_.


1.0 (2018-02-09)
================

- Add a warning to the readme not to use untrusted pickles.

- Drop support for Python 3.3.


0.7.0 (2017-09-22)
==================

- Drop support for Python 2.6 and 3.2.

- Add support for Jython 2.7.

- Add support for Python 3.5 and 3.6.

0.6.0 (2015-04-02)
==================

- Restore the ``noload`` behaviour from Python 2.6 and provide the
  ``noload`` method on the non-C-accelerated unpicklers under PyPy and
  Python 2.

- Add support for PyPy, PyPy3, and Python 3.4.

0.5.2 (2013-08-17)
==================

- Import accelerator from *our* extension module under Py3k.
  See https://github.com/zopefoundation/zodbpickle/issues/6,
  https://github.com/zopefoundation/zodbpickle/issues/7.

- Fix unpickler's ``load_short_binstring`` across supported platforms.

0.5.1 (2013-07-06)
==================

- Update all code and tests to Python 2.6.8, 2.7.5, 3.2.5, 3.3.2 .

- Add the modules ``zodbpickle.fastpickle`` and ``zodbpickle.slowpickle``.
  This provides a version-independent choice of the C or Python
  implementation.

- Fix a minor bug on OS X

0.5.0 (2013-06-14)
==================

- Removed support for the ``bytes_as_strings`` arguments to pickling APIs:
  the pickles created when that argument was true might not be unpickled
  without passing ``encoding='bytes'``, which ZODB couldn't reliably enforce.
  On Py3k, ZODB will be using ``protocol=3`` pickles anyway.

0.4.4 (2013-06-07)
==================

- Add protocol 3 opcodes to the C version of the ``noload()`` dispatcher.

0.4.3 (2013-06-07)
==================

- Packaging error:  remove spurious ``-ASIDE`` file from sdist.

0.4.2 (2013-06-07)
==================

- Fix NameError in pure-Python version of ``Unpickler.noload_appends``.

- Fix NameError in pure-Python version of ``Unpickler.noload_setitems``.

0.4.1 (2013-04-29)
==================

- Fix typo in Python2 version of ``zodbpickle.pickle`` module.

0.4 (2013-04-28)
================

- Support the common pickle module interface for Python 2.6, 2.7, 3.2, and 3.3.

- Split the Python implementations / tests into Python2- and Py3k-specific
  variants.

- Added a fork of the Python 2.7 ``_pickle.c``, for use under Python2.
  The fork adds support for the Py3k ``protocol 3`` opcodes.

- Added a custom ``binary`` type for use in Python2 apps.
  Derived from ``bytes``, the ``binary`` type allows Python2 apps to pickle
  binary data using opcodes which will cause it to be unpickled as ``bytes``
  on Py3k.  Under Py3k, the ``binary`` type is just an alias for ``bytes``.

0.3 (2013-03-18)
================

- Added ``noload`` code to Python 3.2 version of ``Unpickler``.  As with
  the Python 3.3 version, this code remains untested.

- Added ``bytes_as_strings`` option to the Python 3.2 version of
  ``Pickler``, ``dump``, and ``dumps``.

0.2 (2013-03-05)
================

- Added ``bytes_as_strings`` option to ``Pickler``, ``dump``, and ``dumps``.

- Incomplete support for Python 3.2:

  - Move ``_pickle.c`` -> ``_pickle_33.c``.

  - Clone Python 3.2.3's ``_pickle.c`` -> ``_pickle_32.c`` and apply the
    same patch.

  - Choose between them at build time based on ``sys.version_info``.

  - Disable some tests of 3.3-only features.

  - Missing: implementation of ``noload()`` in ``_pickle_32.c``.

  - Missing: implementation of ``bytes_as_strings=True`` in ``_pickle_32.c``.


0.1.0 (2013-02-27)
==================

- Initial release of Python 3.3's pickle with the patches of Python
  `issue 6784`__ applied.

.. __: http://bugs.python.org/issue6784#msg156166

- Added support for ``errors="bytes"``.
