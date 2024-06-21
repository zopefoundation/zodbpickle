import sys

if sys.hexversion >= 0x030c0000:
    from .pickle_312 import *
else:
    from .pickle_38 import *
