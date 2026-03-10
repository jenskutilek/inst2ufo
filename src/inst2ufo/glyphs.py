from typing import TYPE_CHECKING

from ufoLib2.objects.glyph import Glyph

from inst2ufo.pens import RotateStartPointPen

if TYPE_CHECKING:
    from ufoLib2 import Font


def fix_outlines_for_glyphs(ufo: "Font") -> None:
    # Rotate the outlines so that the start point if on an offcurve, like Glyphs does it
    for ufo_glyph in ufo:
        g = Glyph()
        pp = g.getPointPen()
        rsp = RotateStartPointPen(outPen=pp)
        ufo_glyph.drawPoints(rsp)
        ufo_glyph.clear()
        up = ufo_glyph.getPointPen()
        g.drawPoints(up)
