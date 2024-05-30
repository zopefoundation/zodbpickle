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
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    with open(os.path.join(here, fname)) as f:
        return f.read()


README = read('README.rst') + '\n\n' + read('CHANGES.rst')
EXT = 'src/zodbpickle/_pickle_33.c'

# PyPy and jython won't build the extension.
py_impl = getattr(platform, 'python_implementation', lambda: None)
is_pypy = py_impl() == 'PyPy'
is_jython = py_impl() == 'Jython'
is_pure = int(os.environ.get('PURE_PYTHON', '0'))
if is_pypy or is_jython:
    ext_modules = []
else:
    ext_modules = [Extension(name='zodbpickle._pickle',
                             sources=[EXT])]


setup(
    name='zodbpickle',
    version='4.0',
    description='Fork of Python 3 pickle module.',
    author='Python and Zope Foundation',
    author_email='zodb-dev@zope.dev',
    url='https://github.com/zopefoundation/zodbpickle',
    license='PSFL 2 and ZPL 2.1',
    long_description=README,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Zope Public License',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
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
    python_requires='>=3.8',
    extras_require={
        'test': ['zope.testrunner'],
    },
    install_requires=[
        'setuptools',
    ],
    include_package_data=True,
    zip_safe=False,
)
