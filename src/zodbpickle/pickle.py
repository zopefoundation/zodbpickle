import sys

if sys.version_info[0] >= 3:
    from .pickle_3 import *
else:
    from .pickle_2 import *
del sys
