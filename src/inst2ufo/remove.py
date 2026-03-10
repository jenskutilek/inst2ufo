import logging
from typing import TYPE_CHECKING

from ufoLib2 import Font

from inst2ufo.libkeys import LIB

if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


def remove_instructions(ufo_path: "Path") -> None:
    ufo = Font.open(ufo_path)
    logger.info(f"Removing font-level TrueType instructions from '{ufo_path.name}'.")

    if LIB in ufo.lib:
        del ufo.lib[LIB]

    for glyph in ufo:
        if LIB in glyph.lib:
            del glyph.lib[LIB]

    ufo.save(ufo_path, overwrite=True)
