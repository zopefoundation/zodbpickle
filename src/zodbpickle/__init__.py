import sys

if sys.version_info[0] < 3:
    class binary(bytes):
        """Mark a given string as explicitly binary

        I.e., it should be unpickled as bytes on Py3k, rather than being
            forcibly promoted to unicode.
        """
else:
    binary = bytes
