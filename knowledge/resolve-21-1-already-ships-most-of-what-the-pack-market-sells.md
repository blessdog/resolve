---
id: resolve-21-1-already-ships-most-of-what-the-pack-market-sells
kind: verdict
conflict-key: what-motion-and-effect-capability-is-already-installed-before-buying-a-pack
status: live
supersedes: []
verified-on: 2026-09-22
scope: the stock Resolve Studio 21.1.0 install on this MacBook; counts from unzipping Resolve.app/Contents/Resources/Fusion/Templates/Templates.drfx and from the Fusion registry dump; Krokodove and OGraf plugins seen in Contents/Libraries/Fusion/Plugins. The market survey behind the comparison is docs/PLUGIN-ECOSYSTEM-2026-09-22.md; prices there are as of that day
evidence: docs/research-raw/plugins-2026-09-22/motion.md §0 and §5; docs/research-raw/plugins-2026-09-22/ofx-ai.md Appendix A
asked-as:
  - what titles and transitions does Resolve ship
  - do I need a glitch or camera shake pack
  - is Krokodove built into Resolve
  - what does Resolve 21 have for typewriter text or audio reactive animation
  - which plugins should I buy for Resolve
---

**Before any pack is bought or authored, the stock 21.1 install already covers most
of what the pack market sells.** COUNTED on this machine 2026-09-22: 134 Fusion
titles, 67 transitions, 29 effects and 44 generators on the Edit page (unzipped
`Templates.drfx`), 101 ResolveFX by scriptable id (registry dump), and
`krokodove.plugin` + `ograf.plugin` present in the app bundle. DOCUMENTED in the
Resolve 21 New Features Guide and komkomdoorn.com but not yet placed in a comp
here: Krokodove's 100+ tools and its Beat modifier, Lottie/OGraf import, MultiText
CSV import, the Fairlight Animator (audio drives any Fusion parameter), and the
Juggle / Write / From File text modifiers.

What that makes redundant on 21: glitch, camera-shake, crash-zoom and RGB-split
transition packs (all in the stock 67); typewriter and scramble text packs
(Write and Juggle modifiers); tempo pulses and amplitude-driven shake (Beat modifier,
Fairlight Animator); the Krokodove Reactor atom (do not install it on 21);
VHS/retro at the basic level (AnalogDamage, FilmDamage, JPEGDamage, ScanlineV2).

What the market still adds, ranked in the report: gyro stabilisation (Gyroflow,
free), data-driven Fusion from JSON (Vonk Ultra, free, 21 unverified), authentic
NTSC (ntsc-rs, free), seeded retro effects (purzos-ofx, free), camera-matched film
emulation (FilmConvert $119, Filmbox Looks $199), and design polish in title packs
(MotionVFX, whose owner since 2026-03-16 is Apple).

Related: [[the-fusion-page-is-the-only-scriptable-home-for-effects-and-animation]],
[[the-cinematic-levers-ranked-on-the-osmo-exposure-then-optics-then-tone]].
