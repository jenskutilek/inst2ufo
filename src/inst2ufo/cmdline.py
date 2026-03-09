import logging
from argparse import ArgumentParser
from pathlib import Path

from inst2ufo.copy import copy_instructions


def main() -> None:
    parser = ArgumentParser(
        description="Copy TrueType instructions from a binary font to a UFO."
    )
    parser.add_argument(
        "-o",
        "--out",
        type=str,
        nargs=1,
        help="Save UFO to path instead of overwriting the original",
    )
    # parser.add_argument(
    #     "-n",
    #     "--names",
    #     type=str,
    #     nargs=1,
    #     help="Read glyph name mapping from file",
    # )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Verbose output",
    )
    parser.add_argument(
        "ttf",
        type=str,
        nargs=1,
        help="The binary font",
    )
    parser.add_argument(
        "ufo",
        type=str,
        nargs=1,
        help=(
            "The target UFO. If not specified, inst2ufo will look for a UFO with the "
            "same file name stem as the TTF."
        ),
    )
    args = parser.parse_args()
    if args:
        if args.verbose:
            logging.basicConfig(level=logging.INFO)

        ttf_path = Path(args.ttf[0])
        ufo_path = (
            ttf_path.with_suffix(".ufo") if args.ufo is None else Path(args.ufo[0])
        )
        out_path = ufo_path if args.out is None else Path(args.out[0])

        copy_instructions(ttf_path, ufo_path, out_path)

    else:
        parser.print_help()
