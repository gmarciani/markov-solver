#!/usr/bin/env python3

import os

import click

from markov_solver.core.parser.markov_chain_parser import create_chain_from_file
from markov_solver.utils import guiutils, logutils
from markov_solver.utils.report import SimpleReport as Report

logger = logutils.get_logger(__name__)


@click.group(invoke_without_command=True, context_settings=dict(max_content_width=120))
@click.option("--debug/--no-debug", default=False, show_default=True, type=bool, help="Activate/Deactivate debug mode.")
@click.pass_context
@click.version_option(version="1.0.0")
def main(ctx, debug):
    print(guiutils.get_splash())
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
    else:
        logutils.set_log_level(logger, "DEBUG" if debug else "INFO")
        logger.debug("Debug Mode: {}".format("on" if debug else "off"))


@main.command(help="Solve Markov Chain.")
@click.option(
    "--definition",
    required=True,
    type=click.Path(exists=True),
    help="Chain definition file.",
)
@click.option(
    "--outdir",
    default="out",
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def solve(ctx, definition, outdir):
    logger.info("Arguments: definition={} | outdir={}".format(definition, outdir))
    markov_chain = create_chain_from_file(definition)
    states_probabilities = markov_chain.solve()

    report = Report("MARKOV CHAIN SOLUTION")
    for state in sorted(states_probabilities):
        report.add("states probability", state, states_probabilities[state])

    print(report)
    report.save_txt(os.path.join(outdir, "result.txt"), append=True, empty=True)
    report.save_csv(os.path.join(outdir, "result.csv"), append=True, empty=True)

    markov_chain.render_graph(os.path.join(outdir, "MarkovChain"), "svg")
    markov_chain.render_graph(os.path.join(outdir, "MarkovChain"), "png")


if __name__ == "__main__":
    main(obj={})
