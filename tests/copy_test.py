from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from fontTools.cu2qu.ufo import font_to_quadratic
from ufo2ft import compileTTF
from ufoLib2 import Font

from inst2ufo.copy import copy_instructions


class CopyTests(TestCase):
    def test_copy_instructions(self) -> None:
        ps_ufo_path = Path(__file__).parent / "ps.ufo"
        ttf_path = Path(__file__).parent / "tt.ttf"
        tt_ufo_path = Path(__file__).parent / "tt.ufo"
        out_path = Path(__file__).parent / "inst.ufo"

        if tt_ufo_path.exists():
            rmtree(tt_ufo_path)

        # Convert the PS UFO to quadratic curves
        ps_ufo = Font().open(ps_ufo_path)
        font_to_quadratic(ps_ufo, reverse_direction=False)  # not reversing is default
        ps_ufo.save(tt_ufo_path, overwrite=True)
        # Make sure there are no instructions already present
        assert "public.truetype.instructions" not in ps_ufo.lib
        for glyph in ps_ufo:
            assert "public.truetype.instructions" not in glyph.lib
        assert "public.truetype.instructions" not in ps_ufo["o"].lib
        ps_ufo.close()

        # Copy the instructions from the TTF to the converted UFO
        copy_instructions(ttf_path, tt_ufo_path, out_path, fix_glyphs=True)
        out_ufo = Font().open(out_path)
        # Now the UFO should have instructions
        assert "public.truetype.instructions" in out_ufo.lib
        for glyph in out_ufo:
            assert "public.truetype.instructions" in glyph.lib

        # Generate a hinted font
        ttf = compileTTF(
            out_ufo,
            flattenComponents=False,
            inplace=False,
            convertCubics=False,
            rememberCurveType=True,
            removeOverlaps=False,
            reverseDirection=False,
        )
        # ttf.saveXML(out_path.with_suffix(".ttx"))
        ttf.save(out_path.with_suffix(".hinted.ttf"))
        assert "cvt " in ttf
        assert "fpgm" in ttf
        assert "gasp" in ttf
        assert "prep" in ttf
        glyph = ttf["glyf"]["o"]
        assert hasattr(glyph, "program")
        assert len(glyph.program.getBytecode()) == 36

        out_ufo.close()

        # Clean up
        if tt_ufo_path.exists():
            rmtree(tt_ufo_path)
