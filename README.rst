ZODB Pickle
===========

This package is a fork of Python 3.3's pickle module, including its C
optimizations. There are several changes so that ZODBs can be used using
Python 2 and Python 3 code.


Loading/Storing Python 2 Strings
--------------------------------

In all their wisdom, the Python developers have decided that Python 2 ``str``
instances should be loaded as Python 3 ``str`` objects (i.e. unicode
strings). Patches were proposed in Python issue 6784[1] but were never
applied. This code base contains those patches.

..[1] http://bugs.python.org/issue6784


Support for ``noload()``
------------------------

The ZODB uses `cPickle`'s ``noload()`` method to retrieve all persistent
references from a pickle without loading any objects. This feature was removed
from Python 3's pickle. Unfortuantely, this unnecessarily fills the pickle
cache.

This module provides a ``noload()`` method again.
