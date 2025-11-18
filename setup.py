##############################################################################
#
# Copyright (c) 2013 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup"""
import os
import platform

from setuptools import Extension
from setuptools import setup


# PyPy and jython won't build the extension.
py_impl = getattr(platform, 'python_implementation', lambda: None)
is_pypy = py_impl() == 'PyPy'
is_jython = py_impl() == 'Jython'
is_pure = int(os.environ.get('PURE_PYTHON', '0'))
if is_pure or is_pypy or is_jython:
    ext_modules = []
else:
    ext_modules = [Extension(name='zodbpickle._pickle',
                             sources=['src/zodbpickle/_pickle_33.c'])]


setup(ext_modules=ext_modules)
