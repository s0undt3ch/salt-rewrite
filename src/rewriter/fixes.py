"""
Entry point for all the code rewrite fixes.
"""

import importlib.metadata
import operator
from collections import OrderedDict


class RegistryClass:
    """
    Registry class to hold all available fixes.
    """

    __slots__ = ("__fixes__",)

    def __init__(self):
        fixes = []
        for entry_point in importlib.metadata.entry_points(group="fixers"):
            module = entry_point.load()
            fixes.append(
                (getattr(module, "FIX_PRIORITY", 0), module.__name__.split(".")[-1], module)
            )
        __sorted_fixes__ = (
            (name, module) for (_, name, module) in sorted(fixes, key=operator.itemgetter(0))
        )
        self.__fixes__ = OrderedDict(__sorted_fixes__)

    def fixes(self, excluded_names=(), only_names=()):
        """
        Returns all available fixes, optionally skipping those passed in `excluded_names`.
        """
        for name in self.__fixes__:
            if only_names:
                if name in only_names:
                    yield name, self.__fixes__[name]
                continue
            if name in excluded_names:
                continue
            yield name, self.__fixes__[name]

    def fix_names(self):
        """
        Returns the list of the fix names.
        """
        return list(self.__fixes__)


Registry = RegistryClass()
