# -*- coding: utf-8 -*-
"""
    saltrewrite.testsuite.fix_expensive_test_decorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replaces any use of ``@expensiveTest`` with ``@pytest.mark.expensive_test``,
    and, in case ``pytest`` isn't yet imported, it additionall adds the missing
    import
"""
from bowler import Query
from bowler import SYMBOL
from bowler import TOKEN
from fissix.fixer_util import find_indentation
from fissix.fixer_util import Name
from fissix.fixer_util import touch_import
from fissix.pytree import Leaf
from fissix.pytree import Node
from saltrewrite.utils import remove_from_import

MARKER = "pytest.mark.expensive_test"
DECORATOR = "expensiveTest"


def rewrite(paths, interactive):
    query = Query(paths).select("classdef|funcdef")
    # Let's search decorated test classes
    query = query.filter(filter_not_decorated)
    query.modify(replace_decorator).write(interactive=interactive)


def _get_decorator(node):
    """
    Don't modify classes or test methods that aren't decorated with ``DECORATOR``
    """
    if node.parent.type == SYMBOL.decorated:
        child = node.parent.children[0]
        if child.type == SYMBOL.decorator:
            decorators = [child]
        elif child.type == SYMBOL.decorators:
            decorators = child.children
        else:
            raise NotImplementedError
        for decorator in decorators:
            name = decorator.children[1]
            assert name.type in {TOKEN.NAME, SYMBOL.dotted_name}

            if str(name) == DECORATOR:
                return decorator


def filter_not_decorated(node, capture, filename):
    return bool(_get_decorator(node))


def replace_decorator(node, capture, filename):
    """
    Replaces usage of ``@expensiveTest`` with ``@pytest.mark.expensive_test``
    """
    indent = find_indentation(node)

    decorator = _get_decorator(node)
    decorator.remove()

    decorated = Node(
        SYMBOL.decorated,
        [Node(SYMBOL.decorator, [Leaf(TOKEN.AT, "@"), Name(MARKER), Leaf(TOKEN.NEWLINE, "\n")],)],
        prefix=decorator.prefix,
    )
    node.replace(decorated)
    decorated.append_child(node)

    if indent is not None:
        node.prefix = indent
    else:
        node.prefix = ""
    touch_import(None, "pytest", node)
    remove_from_import(node, "tests.support.helpers", "expensiveTest")