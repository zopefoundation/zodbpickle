ZODB Pickle
===========

This package is a fork of Python 3.3's pickle module, including its C
optimizations. There are several changes so that ZODBs can be used using
Python 2 and Python 3 code.


Loading/Storing Python 2 Strings
--------------------------------

In all their wisdom, the Python developers have decided that Python 2 ``str``
instances should be loaded as Python 3 ``str`` objects (i.e. unicode
strings). Patches were proposed in Python `issue 6784`__ but were never
applied. This code base contains those patches.

.. __: http://bugs.python.org/issue6784

Example 1: Loading Python 2 pickles on Python 3 ::

    $ python2
    >>> import pickle
    >>> pickle.dumps('\xff', protocol=0)
    "S'\\xff'\np0\n."
    >>> pickle.dumps('\xff', protocol=1)
    'U\x01\xffq\x00.'
    >>> pickle.dumps('\xff', protocol=2)
    '\x80\x02U\x01\xffq\x00.'

    $ python3
    >>> from zodbpickle import pickle
    >>> pickle.loads(b"S'\\xff'\np0\n.", encoding='bytes')
    b'\xff'
    >>> pickle.loads(b'U\x01\xffq\x00.', encoding='bytes')
    b'\xff'
    >>> pickle.loads(b'\x80\x02U\x01\xffq\x00.', encoding='bytes')
    b'\xff'

Example 2: Loading Python 3 pickles on Python 2 ::

    $ python3
    >>> from zodbpickle import pickle
    >>> pickle.dumps(b"\xff", protocol=0)
    b'c_codecs\nencode\np0\n(V\xff\np1\nVlatin1\np2\ntp3\nRp4\n.'
    >>> pickle.dumps(b"\xff", protocol=1)
    b'c_codecs\nencode\nq\x00(X\x02\x00\x00\x00\xc3\xbfq\x01X\x06\x00\x00\x00latin1q\x02tq\x03Rq\x04.'
    >>> pickle.dumps(b"\xff", protocol=2)
    b'\x80\x02c_codecs\nencode\nq\x00X\x02\x00\x00\x00\xc3\xbfq\x01X\x06\x00\x00\x00latin1q\x02\x86q\x03Rq\x04.'

    $ python2
    >>> import pickle
    >>> pickle.loads('c_codecs\nencode\np0\n(V\xff\np1\nVlatin1\np2\ntp3\nRp4\n.')
    '\xff'
    >>> pickle.loads('c_codecs\nencode\nq\x00(X\x02\x00\x00\x00\xc3\xbfq\x01X\x06\x00\x00\x00latin1q\x02tq\x03Rq\x04.')
    '\xff'
    >>> pickle.loads('\x80\x02c_codecs\nencode\nq\x00X\x02\x00\x00\x00\xc3\xbfq\x01X\x06\x00\x00\x00latin1q\x02\x86q\x03Rq\x04.')
    '\xff'


Support for ``noload()``
------------------------

The ZODB uses `cPickle`'s ``noload()`` method to retrieve all persistent
references from a pickle without loading any objects. This feature was removed
from Python 3's pickle. Unfortuantely, this unnecessarily fills the pickle
cache.

This module provides a ``noload()`` method again.
