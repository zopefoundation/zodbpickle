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

Example 3: everything breaks down ::

    $ python2
    >>> class Foo(object):
    ...     def __init__(self):
    ...         self.x = 'hello'
    ...
    >>> import pickle
    >>> pickle.dumps(Foo(), protocol=0)
    "ccopy_reg\n_reconstructor\np0\n(c__main__\nFoo\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'x'\np6\nS'hello'\np7\nsb."
    >>> pickle.dumps(Foo(), protocol=1)
    'ccopy_reg\n_reconstructor\nq\x00(c__main__\nFoo\nq\x01c__builtin__\nobject\nq\x02Ntq\x03Rq\x04}q\x05U\x01xq\x06U\x05helloq\x07sb.'
    >>> pickle.dumps(Foo(), protocol=2)
    '\x80\x02c__main__\nFoo\nq\x00)\x81q\x01}q\x02U\x01xq\x03U\x05helloq\x04sb.'

    $ python3
    >>> from zodbpickle import pickle
    >>> class Foo(object): pass
    ... 
    >>> foo = pickle.loads("ccopy_reg\n_reconstructor\np0\n(c__main__\nFoo\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'x'\np6\nS'hello'\np7\nsb.", encoding='bytes')
    >>> foo.x
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Foo' object has no attribute 'x'

wait what? ::

    >>> foo.__dict__
    {b'x': b'hello'}

oooh.  So we use ``encoding='ASCII'`` (the default) and ``errors='bytes'`` and
hope it works::

    >>> foo = pickle.loads("ccopy_reg\n_reconstructor\np0\n(c__main__\nFoo\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'x'\np6\nS'hello'\np7\nsb.", errors='bytes')
    >>> foo.x
    'hello'

falling back to bytes if necessary ::

    >>> pickle.loads(b'\x80\x02U\x01\xffq\x00.', errors='bytes')
    b'\xff'


Support for ``noload()``
------------------------

The ZODB uses `cPickle`'s ``noload()`` method to retrieve all persistent
references from a pickle without loading any objects. This feature was removed
from Python 3's pickle. Unfortuantely, this unnecessarily fills the pickle
cache.

This module provides a ``noload()`` method again.