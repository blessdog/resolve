---
id: the-cinematic-levers-ranked-on-the-osmo-exposure-then-optics-then-tone
kind: verdict
conflict-key: what-makes-osmo-footage-look-cinematic-and-in-what-order
status: live
supersedes: []
verified-on: 2026-09-18
scope: DJI Osmo Action 5 Pro, 4K, clips 0001 / 0006 / 0014 (detail measurements) and clip DJI_20260918143132_0002_D window 120-140 s (the four looks), Resolve Studio 21.1 on the MacBook; Ryan's verdict on which look he wants is PENDING
evidence: jobs/film-look-mini/evidence/2026-09-18-osmo-dji-0002-cinematic-options-sheet.jpg; grades/film-look/README.md § What actually makes an image look cinematic; renders in outputs/osmo/2026-09-18-clip-0002/taste/ (gitignored)
asked-as:
  - what makes footage look cinematic
  - which film emulation plugin should I buy for Resolve
  - how do I make action cam footage look like a movie
  - what are my options for a cinematic look in DaVinci Resolve
---

**Ranked by how far each moves the picture on THIS camera: exposure first, optics second,
tone third, colour fourth, texture last. A film emulation plugin is layer four of five,
and the free tools already installed cover layers three to five.**

Layer 1, exposure, MEASURED and by far the largest: sharpness 183 with ND and a locked
1/50 against 13 on the same camera at dusk on auto, a factor of fourteen no plugin closes
([[nd-and-a-locked-shutter-give-the-osmo-real-4k-detail-on-a-still-frame]]).

Layer 2, optics: an action cam's near-infinite depth of field is the strongest non-colour
tell. Verified 2026-09-18 that every relevant ResolveFX adds by script to a clip's Fusion
comp as `ofx.com.blackmagicdesign.resolvefx.<Name>`: CineFocus, DepthMap, LensBlur,
HalationPlugin, Glow, Vignette, CinematicHaze, SoftSharpenSkin, LensDistortion,
ChromaticAberration. Recipe `flc-clean-dof` wires CineFocus; at aperture 0.75 / focus
distance 0.35 it defocused nearly the whole frame, so those numbers are wrong, not the idea.
CineFocus cost 167 s per 20 s of 4K against 34 s for the look alone.

Layer 3, tone: highlight roll-off is where video and film differ. See
[[film-look-creator-on-osmo-clip-0014-blows-the-sky-and-breaks-on-a-dwg-timeline]].

The four looks on the 126 s frame (darkest 1% / brightest 1% / luma std / saturation / at 255):

| look | | | | | | render time, 20 s of 4K |
|---|---|---|---|---|---|---|
| as shot, camera Normal | 23 | 250 | 47.1 | 26.8 | 1.75% | - |
| Film Look Creator restrained, grain off | 40 | 251 | 45.7 | 25.8 | 1.67% | 34 s |
| Film Look Creator 'Cinematic' preset, grain off | 0 | 250 | 58.5 | 24.0 | 1.80% | 38 s |
| Kodak 2383 print fed Cineon log | 19 | 222 | 50.7 | **39.7** | **0.00%** | **8 s** |
| restrained + CineFocus | 44 | 243 | 41.9 | 24.9 | 0.86% | 167 s |

The print is the only one that holds every highlight (nothing at maximum, whites at 222) and
the only one that adds saturation; it is also the cheapest to render, being a LUT on a colour
node rather than a Fusion OFX. The agent's reading of the sheet, not Ryan's: the print reads
richest and most filmic, the Cinematic preset crushes blacks to 0, the restrained look is
very subtle. His eyes are the verdict.

Shooting **Normal rather than D-Log M caps this**: the camera baked its own curve, so 1.75%
of the frame was already at maximum before any grade. The finished workflow wants D-Log M at
these exposure settings.

Market researched 2026-09-18, full table with prices and sources in `grades/film-look/README.md`:
free and installed are Film Look Creator, the print LUTs and utility-dctls; free and NOT
installed is spektrafilm OFX 0.4.7 (35 stocks, grain defeatable, needs an admin password);
paid run $59 to $999 (GrainX, FilmConvert Nitrate $129, Dehancer $179, EMUL8 $196, Filmbox
$199-999); ARRI Film Lab ($25/month) requires LogC input this camera cannot produce.

Related: [[osmo-auto-exposure-picks-fast-shutters-and-high-iso-lock-the-shutter]],
[[a-print-lut-needs-a-cineon-working-space-in-resolve]],
[[film-look-creator-renders-on-the-mini-through-a-fusion-comp]].
