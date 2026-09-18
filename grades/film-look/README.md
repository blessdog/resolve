# film-look — the Osmo Action 5 Pro film grade, from free finished tools

Writer: this session (2026-09-12), then whoever changes a node. Reader: Ryan on
the day the camera lands, and the agent that applies the saved grade later.
Fails when wrong: a node fed the wrong colour space, which looks like a bad
grade and is actually a wrong transform.

Everything here is a downloaded, already-tuned asset. Nothing is hand-rolled.
`manifest.json` is the provenance record (source URL, upstream commit or date,
sha256, license) and `tools/grade-library.py` fetches, installs and verifies it.

    python3 tools/grade-library.py fetch      # into grades/film-look/assets/
    python3 tools/grade-library.py install    # into Resolve's LUT folder, film-look/
    python3 tools/grade-library.py verify     # hashes, repo copy and installed copy
    python3 tools/grade-library.py validate   # Resolve open: compile every DCTL

Installed at `/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/film-look/`.
Resolve lists new files after **LUT browser > Update Lists**, or a restart.

## What is in the library

| Folder | File | What it is | Expects in | Gives out |
|---|---|---|---|---|
| `dji/` | DJI OSMO Action 5 Pro D-Log M to Rec.709 V1.cube | DJI's official conversion. Its header says it is the Mavic 3 Pro LUT | D-Log M | Rec.709 |
| `dji/looks/` | Mei, Ju, Zhu, Lan .cube | DJI's four finished creative looks for this camera | Rec.709 | Rec.709 |
| `melara/` | Rec709_Kodak_2383_D65, Rec709_Kodak_2393_D65, Rec709_Fujifilm_3510_D65 | Juan Melara's free print-stock emulations; the 2383 grey axis is measured identical to Resolve's shipped one | **Cineon Film Log (or ARRI LogC3), Rec.709 primaries** | Rec.709 |
| `thatcher/` | DJI Action 5 D-Log M to DWG.dctl | camera log to DaVinci Wide Gamut, fit to real Action 5 footage | D-Log M | DaVinci Intermediate |
| `thatcher/` | Halation, Film Grain, Film Curve, Subtractive Saturation, Gamut Compression | parameter tools, MIT | scene linear | scene linear |
| `thatcher/` | Printer Lights | per-shot exposure and balance in printer points | log | log |
| `cullen-kelly/` | Kodak 2383 (HUMAN download, see below) | print emulation built for DaVinci Wide Gamut timelines | DWG / DI | Rec.709 |
| Resolve's own `Film Looks/` | Rec709 Kodak 2383 D65.cube and friends | ships with Resolve, not copied | **Cineon Film Log**, Rec.709 primaries | Rec.709 |

## Chain A — camera-day morning (display-referred, all finished LUTs)

Project: DaVinci YRGB, not colour managed. Timeline colour space Rec.709 Gamma 2.4.
`tools/ingest-osmo.py` creates the project and stamps exactly this, and reads
it back. Do not set it by hand; a fresh project otherwise defaults to
"Rec.709 (Scene)".

| Node | On it | Notes |
|---|---|---|
| 1 | Temporal NR | Studio only. NR before anything else so grain later is not NR'd away |
| 2 | LUT: `film-look/dji/DJI OSMO Action 5 Pro D-Log M to Rec.709 V1.cube` | the conversion. Primaries on THIS node apply before the LUT, so exposure and balance corrections here happen in log, which is where they belong |
| 3 | primaries | contrast, saturation, warmth. Taste |
| 4 | LUT: one of `film-look/dji/looks/*.cube`, **or** for a print: CST Rec.709 Gamma 2.4 → Rec.709 gamut / Cineon Film Log, then LUT `film-look/melara/*.cube` | a print LUT fed display Rec.709 instead of log comes out too contrasty and too saturated; Melara's own instructions put the CST to log first. Key output 50 to 70 percent if it bites |
| 5 | Magic Mask, secondaries | only where something needs isolating |
| 6 | Depth Map, Lens Blur | optional, subtle, watch hair edges |
| timeline node | Film Look Creator, grain and halation only | Colour Space Override: input **and** output Rec.709 Gamma 2.4, because everything is display-referred by the time it arrives here |

Save the clip node tree as a PowerGrade named `osmo-film-look-A`, and the
timeline node as `osmo-timeline-A`. Those saved grades are what the scripting
API applies to every clip afterwards (ApplyGradeFromDRX, SetLUT, SetCDL).

## Chain B — scene-referred (DaVinci Wide Gamut), more range, one trap

Project: DaVinci YRGB Color Managed, timeline DaVinci Wide Gamut / Intermediate,
output Rec.709 Gamma 2.4. Set every Osmo clip's input colour space to
**Bypass** so Resolve does not also try its own D-Log guess.

| Node | On it | Notes |
|---|---|---|
| 1 | Temporal NR | as above |
| 2 | DCTL: `film-look/thatcher/DJI Action 5 D-Log M to DWG.dctl` | output DaVinci Intermediate, DaVinci Wide Gamut. **Not** the CST's "DJI D-Log" entry, which is the older Mavic curve |
| 3 | DCTL: `Printer Lights.dctl` or CDL | per-shot exposure and balance, in log |
| 4 | CST: DaVinci Intermediate to Linear (same gamut) | the Thatcher effects want linear |
| 5 | DCTL: `Subtractive Saturation.dctl`, then `Halation.dctl` | linear in, linear out |
| 6 | CST: Linear to DaVinci Intermediate | back to log for the print |
| 7 | **Print, two choices** | (a) Cullen Kelly 2383: DWG in, Rec.709 out, done. (b) Resolve's shipped Kodak 2383: **first** a CST from DaVinci Wide Gamut / Intermediate to **Rec.709 gamut with Cineon Film Log gamma**, then the LUT. Feeding the shipped LUT DaVinci Intermediate directly is the mistake every forum thread on this subject is about |
| timeline node | Film Look Creator grain and halation, or Thatcher `Film Grain.dctl` | if using FLC, set its colour space to what enters it |

Melara's LUTs go exactly where Resolve's shipped 2383 goes in node 7 (b): after
the CST to Rec.709 gamut / Cineon Film Log. They are numerically the same curve.

## Chain C — Ryan's approved look (utility-dctls, scene-linear)

Approved 2026-09-12 on iPhone clip IMG_0006: *"img-0006-rich-halation-grain-400.mp4 looks good."*
Built only from the utility-dctls DCTLs, wired in the clip's Fusion comp by
`jobs/film-look-mini/dctl_film_mini.py`, which builds this recipe when none is named.
The project is colour managed with a Rec.709 / Linear timeline and Rec.709 / Gamma 2.4 output.

| stage | DCTL | settings |
|---|---|---|
| 1 | Clamp | min 0, max off |
| 2 | Halation | reflection exposure lost -5 |
| 3 | Clamp | min 0, max off (stops speckles on saturated colour) |
| 4 | Film Grain (negative) | D max 2.6, 400 grains per pixel |
| 5 | Multiplication Function | gain solved by `film_chain.py` so 0.18 stays 0.18 |
| 6 | Film Curve (print) | gamma 2.8, D min 0.06, D max 3.2 |

Knobs and what they do, measured: `jobs/film-look-mini/evidence/2026-09-12-img-0006-knob-ladder-sheet.jpg`.
Reference frame: `evidence/2026-09-12-approved-look-img-0006-before-after.jpg`.

**Osmo D-Log M** (`--input dji-action5-dlogm`, 2026-09-16). Colour management has no D-Log M input, so
two stages run ahead of stage 1, and the clip's input is set to `Linear` so Resolve passes the code values through:

| stage | DCTL | settings |
|---|---|---|
| 0 | Fusion Resize | to the timeline size, so grain is drawn on the pixel grid the look was approved on |
| A | DJI Action 5 D-Log M to DWG | Output Transfer Function Linear, Output Color Gamut DaVinci Wide Gamut |
| B | Gamut Primaries Conversion | DaVinci Wide Gamut to Rec. 709 |

First clip: `jobs/film-look-mini/evidence/2026-09-16-osmo-dji-0001-dlogm-approved-look-sheet-scaled-first.jpg`
(grain 3.28 against the approved 3.60). The `...-sheet.jpg` beside it was made before stage 0 existed and shows
the thin grain (1.60). No verdict from Ryan on that clip. On the second clip (0004, indoor, about ISO 3200) he
rejected it: "looks like shit" (`knowledge/the-approved-film-look-fails-on-osmo-clip-0004.md`). Do not use Chain C
as the Osmo default.

## What actually makes an image look cinematic (researched 2026-09-18)

Written because Ryan asked to be taught the landscape, not handed a preset. The order
is by **how much each layer moves the picture on THIS camera**, which is not the order
the internet teaches. A film emulation plugin is layer four of five.

### 1. Exposure discipline — the biggest lever, and it is free

MEASURED here on three Osmo clips (`knowledge/osmo-auto-exposure-picks-fast-shutters-and-high-iso-lock-the-shutter.md`,
`knowledge/nd-and-a-locked-shutter-give-the-osmo-real-4k-detail-on-a-still-frame.md`).
Sharpness, and how much a 1080p round trip changes the frame (higher = more real 4K detail):

| clip | settings | sharpness | 1080p round trip |
|---|---|---|---|
| 0002, 2026-09-18 14:31, still frame | ND, 1/50, ISO 100-800 | **183** | **2.21 codes** |
| 0001, 2026-09-16, daylight | auto, 1/2000 | 136 | 1.50 |
| 0006, 2026-09-18 09:14, street ride | auto, 1/500, ISO 800-1600 | 102 | 0.91 |
| 0014, 2026-09-17, dusk ride | auto, 1/330-1/500, ISO 3200-6400 | 13 | 0.38 |

Fourteen times the detail between the worst and best clip, and **no plugin closes that gap**.
Noise reduction cannot restore detail that was never recorded. This is why the ND filters
and the locked shutter were worth more than everything below them combined.

### 2. Optics — what says "action cam" no matter what the colour does

A 1/1.3-inch sensor behind a 155-degree lens has near-infinite depth of field. Everything
is sharp, so nothing is *chosen*, and the eye reads surveillance rather than cinema. Two fixes,
both already installed and both scriptable as Fusion OFX (verified 2026-09-18, ids below):

| what | ResolveFX | why it matters |
|---|---|---|
| shallow depth of field | `CineFocus` (`apertureEnhanced`, `focusDistance`, `focusExtendRange`) or `DepthMap` + `LensBlur` | separates subject from background, the single strongest non-colour cue |
| narrower field of view | dewarp in camera, or `LensDistortion` + a crop | the wide look is the action-cam signature |
| vignette | `Vignette` | pulls the eye to centre; wide lenses need it more |
| atmosphere | `CinematicHaze` (depth-aware) | depth separation without defocus |
| chromatic fringing, softened skin | `ChromaticAberration`, `SoftSharpenSkin` | lens character, faces |

All take `ofx.com.blackmagicdesign.resolvefx.<Name>` and are added to a clip's Fusion comp,
never the colour page (`knowledge/film-look-creator-renders-on-the-mini-through-a-fusion-comp.md`).

### 3. Tone — highlight roll-off is where "video" lives

The one measurable difference between a video image and a film image is what happens
approaching white. Video clips: everything above the limit becomes one flat value. Film
compresses, so a bright sky keeps texture. MEASURED on Osmo clip 0014: the Thatcher D-Log M
conversion, which applies no tone curve, put 24% of a dusk frame at code 255 while DJI's own
LUT (which has a roll-off built in) held the same frame at 1.5%
(`knowledge/film-look-creator-on-osmo-clip-0014-blows-the-sky-and-breaks-on-a-dwg-timeline.md`).
No emulator downstream recovers a sky that is already flat white.

The tools that own this step are called **display rendering transforms (DRTs)**:
Resolve's own DaVinci tone mapping, ARRI Reveal, **OpenDRT** and the **2499 DRT** (both free
DCTLs). This is the layer to fix before judging any look.

**Shooting Normal instead of D-Log M moves this decision into the camera**, which bakes its
own curve and throws the rest away. Normal is right for testing stabilisation; D-Log M at
these exposure settings is what the finished workflow wants.

### 4. Colour — print emulation and the film "look"

Only now does film emulation earn its place. Three families, in rising cost:

- **A print LUT**: Kodak 2383, Fuji 3513. Resolve ships them; Juan Melara's free set is in
  this library and measured identical on the grey axis. **They expect Cineon Film Log input**,
  which is the mistake every forum thread is about (`knowledge/a-print-lut-needs-a-cineon-working-space-in-resolve.md`).
- **Resolve's own Film Look Creator**: a full ResolveFX with core looks, highlight roll-off,
  subtractive saturation, split tone, halation, bloom, grain, flicker, gate weave, film gate.
  Free with Studio, scriptable, 80 s per 20 s of 4K on the MacBook.
- **A photochemical emulator**: models the negative, the print, and the chemistry between them.
  The table below.

### 5. Texture — grain, halation, bloom, gate weave

Ryan, 2026-09-18: *"I'm not looking for the film grain because the quality is not already
grainy."* Correct instinct on clean 4K, and the reason every recipe named `flc-clean-*` sets
`grainIsEnable` 0. Halation (red bleed around highlights) and a little bloom survive that cut,
because they are optical, not chemical, and they read as lens rather than film stock.

---

## The emulator market, priced (researched 2026-09-18)

Status: CHECKED = verified here. REPORTED = the vendor or a review says so.

| Tool | Price | Resolve | Grain defeatable | Notes | Status |
|---|---|---|---|---|---|
| **Film Look Creator** | included with Studio | Studio | yes (`grainIsEnable` 0) | already proven by script here; the place to start | CHECKED |
| **Melara / Resolve print LUTs** | free | free + Studio | n/a | installed; need a Cineon working space | CHECKED |
| **utility-dctls** (Thatcher Freeman) | free, MIT | free + Studio | yes | installed; the parts, not a finished look. REJECTED on DJI footage | CHECKED |
| **spektrafilm OFX** 0.4.7 | **free** (beta) | free + Studio | yes, texture controls | 35 negative stocks (Vision3, Portra, Ektar, Double-X) + 11 prints, halation, diffusion presets modelling Black Pro-Mist, printer lights, MTF, lens distortion. **Strongest free candidate.** Needs an admin password to install into `/Library/OFX/Plugins` | CHECKED (not installed) |
| **OpenDRT**, **2499 DRT** | free | free + Studio | n/a | display transforms, layer 3 above, not emulators | REPORTED |
| **GrainX** | $59 | free + Studio | it *is* grain | scanned Kodak grain, not modelled. Not wanted here | REPORTED |
| **FilmConvert Nitrate** | $129 | free + Studio | yes | camera-profile driven, simplest workflow; check the Osmo is profiled | REPORTED |
| **Dehancer Film** | $179 | free + Studio | yes | the popular choice; well regarded halation, DWG/Intermediate and Cineon aware | REPORTED |
| **EMUL8** (cinem8) | $196 | Studio only | yes | 15 stocks, real-time | REPORTED |
| **Filmbox** (Video Village) | $199 Looks, $999 Pro | Studio only | yes | 98 stocks across 7 photochemical systems; reviewers call it the most accurate | REPORTED |
| **ARRI Film Lab** | $25/month | Studio | yes | **requires LogC3/LogC4 input** — a conversion step this camera does not have. Skip | REPORTED |

Sources: [xeremy comparison](https://xere.my/comparisons/best-davinci-film-grain-plugins/),
[spektrafilm](https://spektrafilm.114c.de/), [Filmbox](https://videovillage.com/filmbox/),
[Dehancer](https://www.dehancer.com/), [FilmConvert Nitrate](https://www.filmconvert.com/nitrate),
[ARRI Film Lab on CineD](https://www.cined.com/arri-film-lab-announced-real-time-analog-film-emulation-plugin-for-davinci-resolve-baselight-nuke/),
[PixelTools free DCTLs](https://pixeltoolspost.com/pages/free-toolkit-for-davinci-resolve).

**The recommendation, in order:** finish Film Look Creator (free, installed, already scripted),
then install spektrafilm (free, one admin password). Buy nothing until those two have been
judged on real footage — which is Ryan's own 2026-09-12 instruction, and the reason row 26 of
`docs/CINEMATIC-PIPELINE-VERIFY.md` exists.

## Candidates not yet in the library (searched 2026-09-16)

Found after Chain C failed on Osmo clip 0004. Nothing below is installed or rendered yet. Status words:
CHECKED (read or verified here), REPORTED (the vendor or a review says so).

| Candidate | What it is | Fits this lane because | Status |
|---|---|---|---|
| **spektrafilm OFX** 0.4.7 ([site](https://spektrafilm.114c.de/), [repo](https://github.com/chaert-s/spektrafilm-ofx)) | a free spectral film simulation: camera negative, then print, with grain, halation, diffusion. 35 stocks incl. Kodak Vision3 50D/250D/200T/500T; prints 2383, 2393 | a finished emulator instead of parts we wire. Its Input Color Space takes DaVinci Intermediate WideGamut, which the D-Log M DCTL outputs. Output Role "Display Out SDR" to Rec.709 Gamma 2.4, or "RCM/ACES" back to the working space | CHECKED: GPL-3.0; pkg signed "Developer ID Installer: Aedan Diez (3495LZ53BZ)" and notarized 2026-09-09; zip sha256 39c94770…; installs spektrafilm, spektrafilm_flow and spektrafilm_lens into `/Library/OFX/Plugins` (admin password); Studio only per its install notes. UNKNOWN: whether a script can add it to a Fusion comp, and under what id |
| **OpenDRT** ([repo](https://github.com/jedypod/open-display-transform)) | a free display-rendering DCTL with look presets | runs through the existing DCTL stage system, no admin | REPORTED |
| **JP-2499 DRT** ([repo](https://github.com/JuanPabloZambrano/DCTL/tree/main/2499_DRT)) | a free film-inspired image formation DCTL, not a film emulation | same | REPORTED |
| **Jamie Fenn DWG 2383 and Fuji 351** ([page](https://www.jamiefenn.com/p/free-dwg-film-emulation-luts/)) | free print LUTs for DaVinci Wide Gamut | the Chain B node 7 slot | REPORTED |
| **ProColor free 2383** ([page](https://procolor.ist/freelut/)) | a free scene-referred 2383 for DWG or ACES | same | REPORTED |
| **Mononodes free PowerGrades** ([page](https://mononodes.com/film-emulation/)) | .drx photochemical emulation | `ApplyGradeFromDRX` applies .drx by script | REPORTED |

Already here and never rendered on Osmo footage: DJI's own D-Log M cube and its four looks, Melara prints fed
Cineon, Resolve's Film Looks folder, Film Look Creator.

## The one human download

Cullen Kelly's free Kodak 2383 for DaVinci Wide Gamut sits behind an email form
at https://freelut.cullenkellycolor.com/. Save the .cube into
`grades/film-look/assets/cullen-kelly/` and run `install` again. Everything
else in the library was fetched by the tool.

## Camera settings that decide more than any node

- D-Log M, 10-bit. Always.
- 24p or 25p. 60p only for shots meant to be slowed.
- Shutter 1/48 or 1/50. Outdoors that needs ND: sunny at ISO 100 is ND64,
  overcast ND8 to ND16. DJI's ND 8/16/32/64 set fits this camera.
- Slow shutter plus max RockSteady smears. One or the other.
- Sharpness and in-camera NR at minimum.
- ISO ceiling 1600 for graded work (chosen line; reviews call 3200+ destructive).
  Clip 0004 (2026-09-16) broke four lines of this list under auto exposure: 29.97, shutter 1/110 to 1/200,
  about ISO 3200, and Ryan read the result as low light (`knowledge/osmo-clip-0004-was-shot-at-about-iso-3200.md`).
  Read a clip's settings with `exiftool -ee -u -G3 -s -n -ShutterSpeed -Dvtm_ac204_3-2-3-1 <clip>`.
- Dewarp or narrower field of view. The 155 degree look reads action-cam regardless.

## What has been verified and what has not

Verified (2026-09-12): every fetched file matches its recorded sha256, both the
repo copy and the installed copy; the two zips list the cubes recorded in the
manifest. `validate` asks Resolve to compile each DCTL.

Not verified: how any of this LOOKS. There is no D-Log M footage on this machine
yet. The first clip off the camera is the test, and the verdict is Ryan's eyes.

iPhone clips (Apple Log, Apple Log 2): the same chains apply. Chain A node 2 becomes a CST node (Apple Log → Rec.709 Gamma 2.4, Resolve has it natively); chain B node 2 is `thatcher/Apple Log 2 to DWG.dctl` (iPhone 17 Pro) or `Apple Log to DWG.dctl` (15/16 Pro).
