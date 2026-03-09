import logging
from typing import TYPE_CHECKING

from fontTools.ttLib import TTFont
from ufoLib2 import Font

if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


def copy_instructions(ttf_path: Path, ufo_path: Path, out_path: Path) -> None:
    font = TTFont(ttf_path)
    ufo = Font.open(ufo_path)
    logger.info(ufo)
