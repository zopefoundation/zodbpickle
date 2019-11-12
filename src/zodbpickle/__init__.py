import sys

__all__ = [
    'binary',
]

if sys.version_info[0] < 3:
    try:
        from zodbpickle._pickle import binary
    except ImportError:
        # we get ImportError if the module isn't around at all,
        # e.g., on PyPy. We get AttributeError if it doesn't define
        # the binary attribute, which would be the case if we have an
        # old version of the C extension library. That might happen in
        # development but shouldn't in production; let it raise.
        class binary(bytes):
            """Mark a given string as explicitly binary

            I.e., it should be unpickled as bytes on Py3k, rather than being
            forcibly promoted to unicode.
            """
            __slots__ = ()
else:
    binary = bytes
