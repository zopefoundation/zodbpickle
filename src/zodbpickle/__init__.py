# Make a package.

class binary(bytes):
    """Mark a given string as explicitly binary

    I.e., it should be unpickled as bytes on Py3k, rather than being
          forcibly promoted to unicode.
    """
