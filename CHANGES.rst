CHANGES
=======

0.1.1 (unreleased)
------------------

- Add support for Python 3.2:

  - Move ``_pickle.c`` -> ``_pickle_33.c``.

  - Clone Python 3.2.3's ``_pickle.c`` -> ``_pickle_32.c`` and apply the
    same patch.

  - Choose between them at build time based on ``sys.version_info``.

  - Disable some tests of 3.3-only features.


0.1.0 (2013-02-27)
------------------

- Initial release of Python 3.3's pickle with the patches of Python
  `issue 6784`__ applied.

.. __: http://bugs.python.org/issue6784#msg156166

- Added support for ``errors="bytes"``.
