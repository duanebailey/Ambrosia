#!/usr/bin/env python3
# Project Ambrosia (c) 2013-19 duane a. bailey
#
"""Ambrosia decorators.

This module defines the decorators that are used in the definition of
ambrosia.
   @checkdoc - check class for appropriate documentation
            (active when CHECKDOC environment variable is set)
"""

import os
from functools import wraps

__all__ = ["checkdoc"]

_require_documentation = bool(os.getenv("CHECKDOC"))

def checkdoc(cls):
    """Check that all methods defined in a class contain documentation.

    This method is a class decorator.  It is used, for example, as
      @checkdoc
      class Tranform...
    When the CHECKDOC environment variable is True, it verifies that 
    all the methods of the indicated class are at least minimally 
    documented. If a public method (one not beginning with underscore)
    does not have an associated docstring, a warning is printed."""
    classname = cls.__name__
    if _require_documentation and not classname.startswith("_"):
        methods = [x for x in dir(cls) if not x.startswith("_")]
        for m in methods:
            docstr = eval("cls."+m+".__doc__")
            if not docstr:
                print("NOTE: Class method {}.{} is not documented.".format(classname,m))
    return cls
