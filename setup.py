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
import sys

from setuptools import Extension, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = (open(os.path.join(here, 'README.rst')).read()
          + '\n\n' +
          open(os.path.join(here, 'CHANGES.rst')).read())

if sys.version_info[:1] < (3,):
    EXT = 'src/zodbpickle/_pickle_27.c'
else:
    EXT = 'src/zodbpickle/_pickle_33.c'

# PyPy and jython won't build the extension.
py_impl = getattr(platform, 'python_implementation', lambda: None)
is_pypy = py_impl() == 'PyPy'
is_jython = py_impl() == 'Jython'
is_pure = 'PURE_PYTHON' in os.environ
if is_pypy or is_jython or is_pure:
    ext_modules = []
else:
    ext_modules = [Extension(name='zodbpickle._pickle',
                             sources=[EXT])]


setup(
    name='zodbpickle',
    version='1.0.1.dev0',
    description='Fork of Python 3 pickle module.',
    author='Python and Zope Foundation',
    author_email='zodb-dev@zope.org',
    url='https://github.com/zopefoundation/zodbpickle',
    license='PSFL 2 and ZPL 2.1',
    long_description=README,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Zope Public License',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Jython',
        'Framework :: ZODB',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
    ],
    keywords='zodb pickle',
    platforms=['any'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=ext_modules,
    extras_require={
        'test': [],
        'testing': ['nose', 'coverage'],
    },
    test_suite='zodbpickle.tests.test_pickle.test_suite',
    install_requires=[
        'setuptools',
    ],
    include_package_data=True,
    zip_safe=False,
)
