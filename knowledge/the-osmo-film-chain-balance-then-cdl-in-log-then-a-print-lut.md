---
id: the-osmo-film-chain-balance-then-cdl-in-log-then-a-print-lut
kind: procedure
conflict-key: how-to-make-osmo-footage-look-cinematic
status: live
supersedes: []
verified-on: 2026-09-18
applies-when: DJI Osmo Action 5 Pro footage (Normal or D-Log M) needs a rich, film-like grade rendered by script, with no grain
not-when: the clip is an iPhone Apple Log clip (ryan-approved-the-utility-dctls-film-look-with-400-grain covers that), or grain is wanted
route: jobs/film-look-mini/auto_balance.py <clip> <tag> <recipe> --timeline cineon solves the channel gains, then dctl_film_mini.py --timeline cineon --recipes <recipe> --print-lut "Film Looks/Rec709 Kodak 2383 D65.cube", and TimelineItem.SetCDL({NodeIndex 1, Slope 1, Offset 0, Power 1.10-1.14, Saturation 1.5-1.7}) for the density. Render with colorSpaceOutputGamma switched back to Gamma 2.4.
sibling: none
asked-as:
  - how do I make the DJI Osmo footage look cinematic
  - the grade looks flat and desaturated
  - what is the node order for a film look
  - how to make footage vibrant not muted
---

**Balance first, grade in log, print last. Three stages, each in the place a lab puts it:**

| stage | where | what |
|---|---|---|
| 1 balance | Fusion comp, `ColorGain` | solved channel gains that make the frame neutral |
| 2 density | colour node 1, `SetCDL` | saturation 1.5 to 1.7, power 1.10 to 1.14, IN LOG |
| 3 print | colour node 1 LUT | Kodak 2383, which runs after the node's primaries |

Measured on clip DJI_20260918143132_0002_D at 60 s (HSV saturation, cast-insensitive):

| | colour | blacks | whites |
|---|---|---|---|
| as shot | 26.6% | 28 | 255 |
| balance + print, no density | 24.3% | 27 | 218 |
| + saturation 1.3, power 1.05 | 31.2% | 23 | 213 |
| + saturation 1.5, power 1.10 | **36.9%** | 20 | 207 |
| + saturation 1.7, power 1.14 | 42.1% | 18 | 203 |

Three things that had to be got right, each of which produced a rejected image first:

- **The balance is SOLVED, not guessed.** `auto_balance.py` loops set-gains, export-still,
  measure, correct; the clip's blue cast went from 13.2 display codes to 0.9 in four passes.
  A look laid over an unbalanced shot spends its range fighting the cast.
- **Density goes in LOG, on the colour node, not in the Fusion comp.** Fusion's
  `BrightnessContrast` pivots contrast around 0, so raising it in a Cineon working space
  crushed the frame to black (`bal-push-1/2/3`, blacks at 4). A CDL on the node runs before
  the node's LUT, which is exactly the lab order: grade the negative, then print it.
- **`SetCDL` is a method of TimelineItem, not of the node graph.** The graph object has
  `SetLUT` but no `SetCDL`, and calling it there raises `TypeError: NoneType is not callable`.

**Saturation measured as mean(max-min channel) is wrong**: it counts a global colour CAST as
colour, so balancing a blue frame made that number fall while the image got better. Use HSV S.

Related: [[a-print-lut-needs-a-cineon-working-space-in-resolve]],
[[i-kept-tuning-film-look-creator-after-it-had-already-been-rejected]],
[[the-cinematic-levers-ranked-on-the-osmo-exposure-then-optics-then-tone]].
