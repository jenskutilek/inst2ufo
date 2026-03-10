# inst2ufo – Copy TrueType instructions from a binary font to a UFO

## Glyphs Hinting To UFO Workflow

Convert the UFO from cubic to quadratic curves and save it as `tt.ufo`:

```sh
fonttools cu2qu --keep-direction ps.ufo -o tt.ufo
```

Open `tt.ufo` in Glyphs, save it as a Glyphs file (because TrueType instructions don't persist in a UFO saved by Glyphs) and hint it using the TrueType Instructor tool.

Export a TTF font from Glyphs. Don't remove overlaps while exporting.

Copy the instructions from the TTF back to the UFO:

```sh
inst2ufo -g myfont.ttf tt.ufo
```

The `-g` option causes the UFO to be modified to match the contours exported to the TTF by Glyphs. If you modify the hinting in the Glyphs file and export the TTF again, update the instruction code in the UFO by running the command without the `-g` option:

```sh
inst2ufo myfont.ttf tt.ufo
```

Now you can generate a font with instructions from the UFO using fontmake:

```sh
fontmake -u tt.ufo -o ttf --keep-direction --keep-overlaps --output-path myfont-hinted.ttf
```

If you need to remove TrueType instructions from a UFO, you can use this command:

```sh
rmufoinst tt.ufo
```

## Copyright

© 2026 by Jens Kutílek
