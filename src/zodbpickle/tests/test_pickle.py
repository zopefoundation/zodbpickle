import sys

if sys.version_info[0] >= 3:
    from .test_pickle_3 import test_suite
else:
    from .test_pickle_2 import test_suite
