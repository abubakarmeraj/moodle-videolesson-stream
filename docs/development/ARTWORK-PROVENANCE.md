# Original ValeLMS artwork

Created2026-10-07 for RC1; retained for RC2 by the ValeLMS project using agent-assisted,
hand-authored vector markup. The owner explicitly authorized replacement and the
GPL-3.0-or-later grant. No inherited image was traced/copied, no stock image/font,
third-party logo, remote image, or image-generation model was used.

| File | Original design / derivation |
|---|---|
| plugin/mod_videolessonstream/pix/monologo.svg | New24×24 video screen/play triangle and open-book geometry |
| plugin/mod_videolessonstream/pix/monologo.png | Transparent24×24 PNG derived from the new SVG |
| plugin/mod_videolessonstream/pix/thumbnail.png | New120×120 lesson placeholder, derived from thumbnail.svg |
| plugin/mod_videolessonstream/pix/thumbnail.svg | New120×120 editable original source for the PNG |

Filename/dimension contracts are retained for the three replaced files. Raster
derivation uses scripts/render_artwork.py, Pillow12.3.0, 4× oversampling/Lanczos;
it reads only simple authored SVG rect/polygon primitives, no external assets.
Both SVGs carry copyright2026ValeLMS contributors and GPL-3.0-or-later SPDX declarations.
The project license applies to raster derivatives. Hashes are in the current
product manifest. RC1 hashes and notices remain in the immutable RC1 tag and docs/release/rc1. Only SVG titles/notice metadata and the controls filename change; geometry/raster artwork is retained.
pix/videolesson-controls.svg is the already accepted original project asset and
was not redesigned. No runtime image-generation/rendering dependency is added.
