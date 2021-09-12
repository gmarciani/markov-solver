#!/usr/bin/env python3

import click

from markov_solver.utils import guiutils, logutils

logger = logutils.get_logger(__name__)


@click.group(invoke_without_command=True, context_settings=dict(max_content_width=120))
@click.option("--debug/--no-debug", default=False, show_default=True, type=bool, help="Activate/Deactivate debug mode.")
@click.pass_context
@click.version_option(version="0.0.1")
def main(ctx, debug):
    print(guiutils.get_splash())
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
    else:
        logutils.set_log_level(logger, "DEBUG" if debug else "INFO")
        logger.debug("Debug Mode: {}".format("on" if debug else "off"))


if __name__ == "__main__":
    main(obj={})
