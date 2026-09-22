---
id: a-reference-matched-lut-already-carries-the-white-balance
kind: verdict
conflict-key: does-osmo-footage-need-a-balance-node-before-the-matched-lut
status: live
verified-on: 2026-09-21
supersedes: []
scope: Osmo Action 5 Pro dusk footage in Rec.709 (not D-Log M), graded with match-fashion-hm-mkl-hm*.cube on a Rec.709 / Gamma 2.4 managed timeline; clip DJI_20260921184748_0002 at 300 s
evidence: jobs/film-look-mini/evidence/2026-09-21-osmo-0002-look-choice.jpg — four 4K stills; cast-free chroma 10.6% ungraded, 18.9% at 0.75, 22.0% at 1.00, and 18.7% with a 50% grey-world balance ahead of 0.75, whose channel means went R127 G67 B39
asked-as:
  - should I balance the clip before the matched LUT
  - my graded footage came out way too orange
  - does the reference-matched cube need a white balance node first
---

**Do not put a balance node in front of a reference-matched LUT. The cube was fitted from a
reference photo's own channel statistics, so it already contains the white balance, and a
grey-world node ahead of it warms the image twice.**

Clip 0002 was shot under a strong blue dusk cast (channel means R80 G99 B121). Grey-world wants
a red gain of 2.19. Applying even half of that (slope 1.480 / 1.023 / 0.732) ahead of
`match-fashion-hm-mkl-hm-0.75.cube` produced means of **R127 G67 B39** — the road, the brick and
the sky all one orange. It gained no colour over the LUT alone (18.7% vs 18.9% cast-free chroma);
the whole difference was cast.

This is a scope limit on [[the-osmo-film-chain-balance-then-cdl-in-log-then-a-print-lut]], not a
contradiction of it: balance-then-look is right when the look is a *print stock* (Kodak 2383 is
scene-neutral and has no opinion about your white point), and wrong when the look is a
*statistical match* to one photograph.

**Measure colour cast-free or the number will argue against your eyes.** Raw HSV saturation
called the milky blue ungraded frame 32.6% and the clean warm graded one 18.0%, because a global
tint is maximally "saturated". Dividing each channel by its own mean before measuring chroma
reverses the ranking to agree with what is on screen: 10.6% → 22.0%. Same trap as
[[cast-insensitive-saturation]] and the reason a grade once looked like it was *removing* colour.

Related: [[match-a-reference-photos-grade-by-baking-color-matcher-into-a-cube]].
