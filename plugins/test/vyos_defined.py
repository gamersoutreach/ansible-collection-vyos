"""
Jinja2 test plugin: vyos_defined

Tests whether a variable is defined, not None, and optionally
matches a specific value or type.
"""

from __future__ import annotations

from functools import wraps

from jinja2.exceptions import UndefinedError
from jinja2.runtime import Undefined

VAR_TYPE_MAP = {
    "str": str,
    "list": list,
    "dict": dict,
    "int": int,
    "bool": bool,
}


def vyos_defined(value, test_value=None, var_type=None):
    """
    Test if a value is defined and not None.

    Optionally check equality to test_value or verify the type.

    Usage in Jinja2:
        x is gamersoutreach.vyos.vyos_defined
        x is gamersoutreach.vyos.vyos_defined(true)
        x is gamersoutreach.vyos.vyos_defined("enable")
        x is gamersoutreach.vyos.vyos_defined(var_type="str")
    """
    if isinstance(value, Undefined) or value is None:
        return False

    if test_value is not None:
        return value == test_value

    if var_type is not None:
        expected_type = VAR_TYPE_MAP.get(var_type)
        if expected_type is None:
            raise ValueError(
                f"vyos_defined: unsupported var_type '{var_type}'. "
                f"Supported types: {', '.join(VAR_TYPE_MAP)}"
            )
        return isinstance(value, expected_type)

    return True


def wrap_test(func):
    """Wrap a test function to catch UndefinedError and return False."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UndefinedError:
            return False

    return wrapper


class TestModule:
    """Ansible test plugin entry point."""

    def tests(self):
        return {
            "vyos_defined": wrap_test(vyos_defined),
        }
