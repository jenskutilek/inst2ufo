import logging
from typing import TYPE_CHECKING

from fontTools.ttLib import TTFont
from ufoLib2 import Font

if TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


LIB = "public.truetype.instructions"
LIB_CVT = "controlValue"
LIB_PREP = "controlValueProgram"
LIB_FPGM = "fontProgram"


def copy_cvt(font: TTFont, ufo: Font) -> None:
    if "cvt " not in font:
        logger.info("The font has no control value table (cvt).")
        return
    cvt = font["cvt "]
    logger.info("Copying control value table")
    ufo.lib[LIB][LIB_CVT] = {str(i): v for i, v in enumerate(cvt.values)}


def copy_fpgm(font: TTFont, ufo: Font) -> None:
    if "fpgm" not in font:
        logger.info("The font has no font program table (fpgm).")
        return
    fpgm = font["fpgm"]
    if not hasattr(fpgm, "program"):
        logger.warning("The fpgm table does not contain a program.")
        return
    logger.info("Copying font program table")
    ufo.lib[LIB][LIB_FPGM] = "\n".join(fpgm.program.getAssembly())


def copy_glyf(font: TTFont, ufo: Font) -> None:
    if "glyf" not in font:
        logger.warning("The font has no glyf table.")
        return

    glyph_set = font.getGlyphSet()
    logger.info("Copying glyph programs")
    for glyph_name in glyph_set.keys():
        if glyph_name not in ufo:
            logger.warning(f"Glyph from font not found in UFO: '{glyph_name}'")
            continue
        ufo_glyph = ufo[glyph_name]
        tt_glyph = font["glyf"][glyph_name]
        if LIB in ufo_glyph.lib:
            logger.warning(
                "Overwriting existing TrueType instructions "
                f"in UFO glyph '{glyph_name}'."
            )
        lib = ufo_glyph.lib[LIB] = {}
        if hasattr(tt_glyph, "program"):
            lib["assembly"] = "\n".join(tt_glyph.program.getAssembly())
        else:
            logger.info(f"Glyph '{glyph_name}' does not contain a program.")
        lib["formatVersion"] = "1"
        lib["id"] = ""


def copy_maxp(font: TTFont, ufo: Font) -> None:
    if "maxp" not in font:
        logger.warning("The font has no maximum profile table (maxp).")
        return
    maxp = font["maxp"]
    logger.info("Copying maximum profile table")
    lib = ufo.lib[LIB]
    lib["maxFunctionDefs"] = maxp.maxFunctionDefs
    lib["maxInstructionDefs"] = maxp.maxInstructionDefs
    lib["maxStackElements"] = maxp.maxStackElements
    lib["maxStorage"] = maxp.maxStorage
    lib["maxTwilightPoints"] = maxp.maxTwilightPoints
    lib["maxZones"] = maxp.maxZones


def copy_prep(font: TTFont, ufo: Font) -> None:
    if "prep" not in font:
        logger.info("The font has no control value program table (prep).")
        return
    prep = font["prep"]
    if not hasattr(prep, "program"):
        logger.warning("The prep table does not contain a program.")
        return
    logger.info("Copying control value program table")
    ufo.lib[LIB][LIB_PREP] = "\n".join(prep.program.getAssembly())


def copy_instructions(ttf_path: Path, ufo_path: Path, out_path: Path) -> None:
    font = TTFont(ttf_path)
    ufo = Font.open(ufo_path)
    logger.info(ufo)

    if LIB in ufo.lib:
        logger.warning("Overwriting existing TrueType instructions in UFO.")

    ufo.lib[LIB] = {}

    copy_cvt(font, ufo)
    copy_fpgm(font, ufo)
    copy_prep(font, ufo)
    copy_maxp(font, ufo)
    copy_glyf(font, ufo)

    if ufo.lib[LIB]:
        ufo.lib[LIB]["formatVersion"] = "1"

    ufo.save(out_path, overwrite=True)
