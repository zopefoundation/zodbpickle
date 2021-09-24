import sys

'''
The zodbpickle.pickle module exposes the standard behavior of
the pickle module.
This is backward compatible, but has the effect that by default,
on Python3 you get the fast implementation, while on Python2
you get the slow implementation.

This module is a version that always exposes the fast implementation
of pickling and avoids the need to explicitly touch internals.
'''

'''
Note: We are intentionally using "import *" in this context.
The imported modules define an __all__ variable, which contains
all the names that it wants to export.
So this is a rare case where 'import *' is exactly the right thing to do.
'''

# pick up all names that the module defines
if sys.version_info[0] >= 3:
    from .pickle_3 import *
    # do not share the globals with a slow version
    del sys.modules['zodbpickle.pickle_3']
else:
    from .pickle_2 import *
# also make sure that we really have the fast version, although
# python3 tries to import them by default
from ._pickle import *

del sys
