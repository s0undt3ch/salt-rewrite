# Rewriter

Rewriter is a fork of [salt-rewrite](https://github.com/saltstack/salt-rewrite), a tool created to
automate, and enforce, some of the code design decisions in the evolution of
[Salt](https://github.com/saltstack/salt) and its test suite.

Some code specific to [Salt](https://github.com/saltstack/salt) has been removed to  make this a more generic tool.

## Extend
Some fixes might not be suited to be included in this project, either because their scope is too narrow, or because,
they might not be allowed to be made public.

For these cases, a separate project, which depends on this one, can be created and in order for the fixes to be made
available to this `rewriter`, simply declare your fixes as an entry-point to the `fixers` group.

### Using Poetry

```toml
[tool.poetry.plugins."fixers"]
fix_asserts = "<my package>.<my fixer module"
```

### Using setuptools `pyproject.toml`

```toml
[project.entry-points."fixers"]
fix_asserts = "<my package>.<my fixer module"
```
