"""
``rewriter``'s CLI interface.
"""

from importlib.metadata import version

import click

from rewriter.fixes import Registry


@click.command()
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
    ),
)
@click.option("--silent/--no-silent", "-s/-S", is_flag=True, default=False)
@click.option("--interactive/--no-interactive", "-i/-I", is_flag=True, default=False)
@click.option("--list-fixes", "-l", is_flag=True)
@click.option(
    "-fix",
    "-F",
    type=click.Choice(Registry.fix_names(), case_sensitive=False),
    multiple=True,
)
@click.option(
    "--exclude-fix",
    "-E",
    type=click.Choice(Registry.fix_names(), case_sensitive=False),
    multiple=True,
)
@click.version_option(version=version("rewriter"))
def rewrite(paths, interactive, silent, list_fixes, fix, exclude_fix):
    """
    Main CLI entry-point.
    """
    if list_fixes:
        click.echo("Fixes:\n{}".format("\n".join(f" - {fix}" for fix in Registry.fix_names())))
        return

    if fix and exclude_fix:
        error = "The --fix and --exclude-fix are mutually exclusive options"
        raise click.UsageError(error)

    for fixname, module in Registry.fixes(excluded_names=exclude_fix, only_names=fix):
        click.echo(f"Running {fixname} ...", err=True)
        module.rewrite(paths, interactive=interactive, silent=silent)
