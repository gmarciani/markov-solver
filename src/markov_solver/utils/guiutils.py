"""
Utilities for CLI.
"""

import sys

from colored import attr, fg  # type: ignore
from pyfiglet import Figlet  # type: ignore

from markov_solver.utils.logutils import get_logger

logger = get_logger(__name__)


def get_splash(name: str) -> str:
    """
    Returns the Splash Screen as ASCII Art.
    :return: The Splash Screen.
    """
    f = Figlet(font="slant")
    return "%s %s %s" % (fg("yellow"), f.renderText(name), attr(0))


def print_progress(
    iteration: int,
    total: int,
    prefix: str = "PROGRESS",
    suffix: str = "Complete",
    message: str = "",
    decimals: int = 0,
    bar_length: int = 50,
) -> None:
    format_string = "{0:." + str(decimals) + "f}"
    percents = format_string.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "=" * filled_length + " " * (bar_length - filled_length)

    sys.stdout.flush()

    sys.stdout.write(
        "\r%s [%s] %s%% %s (%d/%d) { %s }"
        % (prefix, bar, percents, suffix, iteration, total, message or "no message")
    )


if __name__ == "__main__":
    print(get_splash("Program Name"))

    from time import sleep

    tot = 1000

    logger.info("Start")

    for i in range(tot + 1):
        sleep(1 / tot)
        print_progress(i, tot)

    logger.info("End")
