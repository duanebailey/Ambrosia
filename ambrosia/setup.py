# A file for Duane A. Bailey's ambrosia package.
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
long_description = """
AMBROSIA
========

This is the Python-based front-end for the POV renderer, used by
The Art & Science of Computer Graphics at Williams College, taught
by Duane A. Bailey

See http://www.cs.williams.edu/~bailey/Ambrosia."""

setup(
    name='ambrosia',

    version='1.0',

    description='Package for CS109, Williams College, taught by Duane A. Bailey',
    long_description=long_description,

    # The project's main homepage.
    url='http://www.cs.williams.edu/~bailey/Ambrosia',

    # Author details
    author='Duane A. Bailey',
    author_email='bailey@cs.williams.edu',

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Students',
        'Topic :: Computer Graphics :: 3D Modeling',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD 3-Clause License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='computer graphics modeling',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['ambrosia','ambrosia/zoo','ambrosia/examples'],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=[],

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        'structure': ['Makefile',],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [],
    },
)
