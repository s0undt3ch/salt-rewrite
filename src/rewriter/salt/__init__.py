# pylint: disable=missing-module-docstring
from rewriter.salt import fix_docstrings
from rewriter.salt import fix_dunder_utils
from rewriter.salt import fix_warn_until

__all__ = [modname for modname in list(globals()) if modname.startswith("fix_")]

__fixes__ = [
    (getattr(module, "FIX_PRIORITY", 0), module)
    for module in [globals()[modname] for modname in __all__]
]
