---
id: fold-the-d-log-m-highlights-ahead-of-film-look-c
kind: open
conflict-key: should-we-fold-the-d-log-m-highlights-ahead-of-film-look-c
status: live
supersedes: []
proven: false
verified-on: 2026-09-17
asked-as:
  - Fold the D-Log M highlights ahead of Film Look Creator so a dusk sky holds the way DJI's LUT holds it
  - fold the d log m highlights ahead of film look c
  - why is 2026-09-17-osmo-dji-0014-film-look-creator-taste-sheet.jpg like this
---

**This is a PLAN, not a finding. `proven: false`. Do not build against it.**

## Fold the D-Log M highlights ahead of Film Look Creator so a dusk sky holds the way DJI's LUT holds it

**Why it matters:** Measured 2026-09-17 on Osmo clip 0014 at 750 s: FLC after the Thatcher D-Log M DCTL puts 13 to 22% of pixels at 255 (DJI's LUT 1.49%) whichever space FLC is told it receives; the DaVinci WG timeline with DaVinci tone mapping 1000 to 100 nits clipped 26.6% on the conversion alone and FLC rendered white tile-sized blocks there. Until the sky holds, Ryan judges the emulator on a conversion defect, and the full 25-minute render (about 110 min of FLC time) is not worth starting

**Where it lands:** `jobs/film-look-mini/dctl-film-recipes.json and jobs/film-look-mini/evidence/2026-09-17-osmo-dji-0014-film-look-creator-taste-sheet.jpg`

**First step:** Two candidates, one 740-760 s window render each via dctl_film_mini.py: (1) a highlight roll-off stage (CST or DCTL) between the D-Log M DCTL and FLC on the linear timeline; (2) read why 1000-to-100 tone mapping did not fold the --timeline dwg path and why FLC corrupts there (agent's reading: bloom or halation meeting out-of-range values). Compare pixels at 255 against DJI's LUT at 1.49%

Bookmarked 2026-09-17 at the moment of deferral, because the record of a deferral is what fails, not the decision to defer.
