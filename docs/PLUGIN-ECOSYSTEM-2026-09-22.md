# The Resolve / Fusion plugin ecosystem — what other people already built (2026-09-22)

*Report before build. Ryan, 2026-09-22: "Do a search on what plugins exist. There's
probably already a lot of really good stuff that we can utilize that other people
build. Color profiles and animations."* Four research passes ran in parallel
(colour, motion/titles, OFX/AI, scripting/Fuses): 120+ web searches, ~90 page
fetches, GitHub/GitLab API calls, and a live registry dump on this Mac. The raw
tables with every URL are in `docs/research-raw/plugins-2026-09-22/` —
`colour.md`, `motion.md`, `ofx-ai.md`, `scripting.md`. This file is the distilled
verdict layer. **VERIFIED** = read on a vendor/primary page or measured here.
**UNVERIFIED** = seen only in a search summary or reseller blurb.

Machine: DaVinci Resolve **Studio 21.1.0**, Apple Silicon MacBook, macOS 27.
Installed third-party today: spektrafilm OFX (4 bundles, in `~/Library/OFX/Plugins`,
free, GPL) and our own 14 `.setting` titles. Zero Fuses, zero Reactor, zero
community macros, `/Library/OFX/Plugins` does not exist.

---

## 1. The finding that decides everything: the scripting boundary

Everything below is filtered through one question — *can the pipeline place it
without a click?* Verified against the local `DaVinciResolveScript.pyi` (dated
2026-09-07) and a live `fuscript` session on 21.1.0:

| Format | How the API places it | Verdict |
|---|---|---|
| **OFX effect** (ResolveFX or third-party) in a **Fusion comp** | `comp.AddTool("ofx." + <OFX plugin identifier>)` | **SCRIPTABLE. MEASURED**: 101 `ofx.` IDs dumped from `Fusion():GetRegList(CT_Tool)`; `AddTool("ofx.com.blackmagicdesign.resolvefx.Glow")` returned a live `Glow1`. Full ID list: `research-raw/plugins-2026-09-22/ofx-ai.md` Appendix A |
| **OFX effect on the Color page** | none — no `AddNode`, no OFX parameter access | **NOT scriptable.** Only `ApplyGradeFromDRX(path)` replays a saved `.drx`. Dehancer/Filmbox/Neat Video "as normally used" are GUI-only; put them in a Fusion comp if automation matters |
| `.cube` LUT on an existing colour node | `Graph.SetLUT(nodeIndex, path)` | SCRIPTABLE (doc-verified) |
| `.dctl` on a colour node | `SetLUT` with a `.dctl` path | **UNVERIFIED — one-line test owed.** Certain via `.drx`, and certain in Fusion via `ofx.com.blackmagicdesign.resolvefx.DCTL` |
| `.drfx` / `.setting` title, generator, effect (Edit-page Fusion template) | `Timeline.InsertFusionTitleIntoTimeline(name)`, `InsertFusionGeneratorIntoTimeline`, `InsertOFXGeneratorIntoTimeline` | SCRIPTABLE by name once installed in the Effects Library. Our 14 titles are already this case |
| `.drfx` / `.setting` **transition** | `TimelineItem.AddTransition({type, category:"fusion"\|"ofx"\|"simple"\|"audio", position, alignment, duration})` | SCRIPTABLE **on 21.1 only** (new API; in `CHANGELOG.md`) |
| `.setting` macro in `Fusion/Macros/` | `comp.Paste(bmd.readfile(path))` after `AddFusionComp()` | SCRIPTABLE, two-step |
| `.comp` composition | `TimelineItem.ImportFusionComp(path)` — **replaces the comp, emit MediaIn/MediaOut yourself** (`FUSION-LANE.md` §5) | SCRIPTABLE |
| Fuse (`.fuse`) / compiled `.plugin` | appears as a Fusion tool → `comp.AddTool("<ToolID>")` | SCRIPTABLE. Fuses are Lua/DCTL, architecture-neutral |
| Lottie `.lottie` / OGraf `.json` (new in 21) | `MediaPool.ImportMedia` → append as an alpha clip; `OGrafLoader` Fusion node | SCRIPTABLE (inferred, not run) |
| **Timeline keyframes / retime curves** on the Edit page | none — `grep -i keyframe` in the `.pyi` finds only Color dynamics and import options | **NOT scriptable.** Animation by script goes through Fusion comps or templates. `SetProperty("Speed")` is constant speed only |
| Fairlight FX | none | NOT scriptable |
| `.drp` template project (placeholder-swap packs) | `ImportProject` brings the whole thing; swapping is GUI | GUI-only in practice |

Consequence: **the Fusion page is the automation surface.** Anything sold as
"Edit page only" or "Color page only" is a hand tool for Ryan, not a pipeline
part — fine, but it should be bought knowing that.

Edition gates, for the record (we are on Studio, so none bite): external Python,
Workflow Integration panels, UIManager scripts, Reactor's in-app GUI and the native
MCP server are all Studio-only; free 21.1 silently drops `.py` from the Scripts menu.

---

## 2. What Resolve 21.1 already gives us — before installing anything

Measured on this machine unless marked otherwise.

| Already here | Count / detail | Reaches the pipeline via |
|---|---|---|
| **ResolveFX** | **101** OFX tools by verified ID: Glow, Halation, Film Look Creator, Film Grain, Film Damage, Analog Damage, JPEG Damage, Scanlines, Lens Flare, Light Rays, Aperture Diffraction, AI Stylize, AI Cinematic Haze, AI CineFocus, AI Depth Map, AI Relight, AI UltraSharpen, AI Motion Deblur, Pencil Sketch, Watercolor, Camera Shake, Motion Trails, Stop Motion, Video Collage, Warper, DCTL, Surface Tracker, Noise Reduction … | `comp.AddTool("ofx.com.blackmagicdesign.resolvefx.<Name>")` — already how `dctl_film_mini.py` works |
| **Edit-page templates** (`Templates.drfx`, unzipped and counted) | **134 titles, 67 transitions, 29 effects, 44 generators** (21 stinger transitions). Transitions include Camera Shake, Crash Zoom, Zoom In, Glitch, Block Glitch, RGB Splitter, Stretch Blur, Film Strip | `InsertFusionTitleIntoTimeline`, `AddTransition` |
| **Fusion bins** | Styled Text: 3D Follower, Flip/Jiggle/Rotate/Stretch Follower, Scramble Modifier, Odometer, Circle/Path Layout. Tools: Advanced Camera Shake. 523 lens-flare files, 289 particle files, 354 shader files | `comp.Paste` |
| **Krokodove** (was a Reactor atom) | built into 21.0, +25 tools in 21.1 (`krokodove.plugin` verified in the bundle): Duplicate 3D, Kaleidoscope, Fragments, Grow, Seamless Loop, Sort, Painterly, Shapes, Text modifiers **Juggle / Write (typewriter) / From File / Formula**, **Beat** modifier | `comp.AddTool` |
| **Fairlight Animator** modifier (21; 21.1 adds high/low-pass) | any Fusion parameter driven by timeline audio | modifier set via comp |
| **MultiText** (20; CSV import in 21) | many styled layers in one tool — data-driven lower thirds | comp |
| **Lottie / OGraf import** + `OGrafLoader` (21) | the whole LottieFiles / Bodymovin ecosystem as alpha clips | `ImportMedia` (inferred) |
| **Film Look Creator, Color Slice, Chroma Warp, Magic Mask 2, Depth Map 2** | colour-page tools; FLC already measured in the store | `.drx` only on Color page; FLC also as `ofx.…FilmLook` in Fusion |
| **Scripting 21.1** | `AddTransition`, Fades/Speed get/set, presets, Media Pool transcription with speaker timing, DCTL validate, native MCP server | already in use |
| **Grade library** (`grades/film-look/`) | thatcher utility-dctls + dwg-transforms (MIT/open), Melara prints, DJI cubes, Cullen Kelly 2383, spektrafilm OFX | `dctl_film_mini.py` |

Several pack categories people sell are now redundant on 21: glitch/shake/zoom
transitions, typewriter and scramble text, camera shake rigs, tempo pulses.

---

## 3. Recommended free stack — install list, all scriptable

Ordered by how much picture each moves for Ryan's footage (Osmo ride clips,
iPhone Apple Log, music-driven cuts, explainers).

| # | Install | What it is | Format / route | Status |
|---|---|---|---|---|
| 1 | **Gyroflow OpenFX** v2.1.1 — https://docs.gyroflow.xyz/app/video-editor-plugins/davinci-resolve-openfx | gyro-data stabilisation; Osmo Action 4/5 gyro supported; Metal | OFX, macOS dmg → `/Library/OFX/Plugins` (admin) or `~/Library/OFX/Plugins` + `OFX_PLUGIN_PATH` (the spektrafilm route, already proven). Fusion `AddTool` by dumped ID | VERIFIED ships arm64; single biggest quality win on ride footage per the OFX pass |
| 2 | **Reactor Standalone** (Beta 37, 2025-11) — `brew install --cask kartaverse/reactor/reactor` | the package manager for ~470 free Fusion atoms (711 dirs, 238 are BMD version records) | desktop app; atoms land in `…/Fusion/Reactor/Deploy/{Fuses,Macros,Scripts}`; the GitLab API is open, so installs can be scripted without the GUI | docs say Resolve "v15–20+"; **21 support inferred from atoms updated in 2026, not stated** |
| 3 | via Reactor: **Vonk Ultra + FusionMograph** (28 atoms, Mograph v3.2 2026-06-15) | data nodes: `vJSONFromFile` / `vTextFromFile` read JSON/CSV at render time and drive any parameter; 200+ Mograph array/stagger/easing tools | Fuses, GPL-3 | docs stop at 20.2 — **test one node on 21.1 first**. This is the "Python owns the beats.json, Fusion renders" primitive the music lane wants |
| 4 | via Reactor: **Suck Less Audio (WAV)** modifier, **Suck Less Write On**, **Follower In Time**, **Anim Utility**, **Flux Super Transform**, **Echo**, **ExponentialGlow + Flare Tools**, **FUI Designer**, **MT_GlitchTools**, **FrameTools CapCut Captions** (8 titles, 2026-04) | the ten most useful mograph atoms per the motion pass; Follower In Time fixes the constant-duration problem templated titles have | Fuses / `.setting` | 21 UNVERIFIED per atom; all architecture-neutral |
| 5 | **purzos-ofx** v0.2.0 — https://github.com/purzbeats/purzos-ofx | 64 seeded, deterministic retro effects: ASCII, dither, pixel sort, CRT, VHS, datamosh, halation, bloom, duotone | OFX, MIT, **ships `macos-arm64.zip`**; unsigned → `xattr -dr com.apple.quarantine` | VERIFIED build exists; 21.1 not stated |
| 6 | **ntsc-rs** v0.9.6 (2026-09-05) — https://ntsc.rs/docs/openfx-plugin/ | the most authentic free VHS/NTSC; works in Color and Fusion pages | OFX, macOS pkg | VERIFIED |
| 7 | **OpenDRT** v1.1.0 (Jed Smith, GPL-3, pushed 2026-02) — https://github.com/jedypod/open-display-transform | free scene-referred display transform that holds highlights; look presets | DCTL drop into the LUT folder; `grade-library.py` can pin it | REPORTED, not rendered here; candidate for the open bookmark `compare-other-free-film-emulators-on-osmo-d-log-` |
| 8 | **Demystify-Color DCTLs** (MIT, pushed 2026-05) and **xtremestuff/resolve-dctl** (MIT, 2026-04) | maintained, permissively licensed utility DCTLs — the only two in the survey that are both MIT **and** active besides thatcherfreeman | DCTL | REPORTED |
| 9 | **Rodrigo Polo Apple Log 2 → Rec.709** 65-pt cube (free) — https://rodrigopolo.com/2025/11/04/apple-log-2-to-rec-709-conversion-lut/ | the cleanest free technical transform for the iPhone 17 Pro | `.cube` → `Graph.SetLUT` | REPORTED; the CST dropdown may already have Apple Log 2 — **check before adopting** |
| 10 | **AutoSubs** v3.10.1 (MIT, `AutoSubs-Mac-ARM.pkg` 2026-09-19) — https://github.com/tmoroney/auto-subs | on-device transcription + diarisation straight into Text+ subtitles | Tauri app + Lua bridge | VERIFIED release; **conflicts with the Deepgram lock** — a hand tool for Ryan, not a pipeline part |
| 11 | **FLPP** (movalex, MIT) and **fusionscript-stubs** (czukowski, 2026-07) | `.comp`/`.setting` ↔ JSON round-trip without Fusion open; IDE typing for the raw API | Python | small, unmaintained but format-stable / active |
| 12 | **Akascape Fuses** (Super VHS $25, others free): Datamosh, Pixel Sorting, CRT, ASCII, RemBG, Neural Style Transfer | broadest free trendy set; style transfer answers any anime/comic ask that AI Stylize does not | Fuse + local Python for the AI ones | shell-out Fuses are slow; AI Stylize is built in and scriptable — try that first |

Licence note: JP Zambrano's DCTLs (2499 DRT), AgX-Resolve and Baldavenger's DCTLs
are popular but carry **no licence file** or GPL; fine to use, not to vendor into
`grades/` the way we vendor thatcher. Baldavenger's last push was 2023-12 and his
OFX is Intel-only (an arm64 rebuild exists at Demystify-Color, 2026-05).

---

## 4. Paid — ranked by value, with the number

Nothing here is bought without Ryan's verdict. Prices VERIFIED on vendor pages
unless marked.

| Rank | Product | Price | What it buys that free does not | Scriptable? |
|---|---|---|---|---|
| 1 | **FilmConvert Nitrate** (OFX) | **$119** perpetual (RRP $149) | 19 stocks matched per camera profile, grain, halation; cheapest reputable emulation | in Fusion via `ofx.` id; Osmo Action 5 Pro profile UNVERIFIED |
| 2 | **Filmbox Looks** (Video Village) | **$199** perpetual, $69/yr, 14-day trial | the reference Kodak negative+print, one-button tier | in Fusion via `ofx.` id (UNVERIFIED that it registers in Fusion) |
| 3 | **Neat Video for DaVinci Resolve** | Home $89.90 / Pro **$159.90** (reported; vendor page returned 418) | the reference denoiser, when Studio's NR is not enough | Fusion; **buy the "for DaVinci Resolve" edition — the generic OFX edition does not support Resolve** |
| 4 | **Envato Elements Core** | **$16.50/mo** annual | unlimited `.drfx`/`.setting`/`.comp` downloads + fonts + SFX | drfx/setting by name; filter items by format |
| 5 | **Motion Array** | $29.99/mo or $239.88/yr (third-party pricing pages) | the deepest Resolve-native macro catalogue | drfx by name |
| 6 | **sh4rk 3D Text Animator Pro** ($18.90), **Allavio Text Animator** ($14.99), **NeoEditFX Animated Text Pack** ($59) | cheap keyframe-less per-character text | Resolve 19–21.1 stated for sh4rk | titles by name |
| 7 | **MotionVFX DVR packs** (mTitle Mega Pack $139, mTransition Fade $69) | best design polish for Resolve titles | **Apple acquired MotionVFX on 2026-03-16** (Bloomberg, 9to5Mac); still on sale, future unstated | by name once mInstaller places them |
| 8 | **Dehancer Pro** | Individual lifetime **$1,099** on the 2026 pricing page (a Feb 2025 review said $449 — the tiers changed) | the most complete single film plugin | Color page = not scriptable; Fusion UNVERIFIED |
| 9 | **Boris FX Continuum / Sapphire**, **Maxon Red Giant / Universe** | Continuum $365–2,195 perpetual or $32+/mo; Sapphire $1,865; Red Giant $639/yr, Universe $214/yr | Particle Illusion, Beat Reactor, S_Glow, Magic Bullet Looks, Universe VHS/glitch presets | Fusion via `ofx.` id. Continuum states Resolve 21; **Maxon's KB reportedly still says 19/20, not 21** (page blocked, UNVERIFIED). Rent monthly for a job, never own |
| 10 | **Topaz Video** ($299/yr), **Colourlab AI Studio** ($49/mo for the in-Resolve plugins), **Qazi Toolkit** ($776), **RapidGrade** ($699) | — | subscription-only or overpriced against what Studio 21 ships (SuperScale, UltraSharpen, Color Slice) | skip |

---

## 5. Corrections and dead ends — do not search these again

| Assumed | Found |
|---|---|
| "Ground Control" (Casey Faris) sells zoom/shake/speed-ramp packs | it sells **courses**; no preset pack exists (store page 404) |
| "KRIL", "mFusion", "Emery" film emulation, "Dawson Colour", "Chetal"/"Cyclone" Fuse collections, "Rob Ballard", "Alex Fichera", "resolve-toolbox" | **not found** under any phrasing, in Reactor's 711 atoms, GitHub or the web. Likely misremembered names |
| Lenofx, RocketStock | Lenofx is FCP-only; RocketStock redirects to Shutterstock Elements — no Resolve items |
| Mixkit's free Resolve templates | Resolve-16-era `.comp` files; dated |
| Krokodove needs Reactor | built into 21.0; **do not install the atom on 21** |
| openfx-misc (Natron), G'MIC OFX, TuttleOFX as free OFX | no arm64 build loads in Resolve 21 without compiling; TuttleOFX dead since 2020 |
| Frame.io integration | legacy Studio 16/17 only; dead on Frame.io V4 |
| Qazi's "Colorist Factory" | domain no longer resolves |
| Mononodes "free" DCTLs | a paid store (free PowerGrades exist separately) |
| Spektrafilm needs an admin password | it does not — user-dir install proven (store claim `spektrafilm-installs-without-admin…`); its **parameters** are the unsolved part |

---

## 6. Hazards worth carrying into every install

- **`ImportFusionComp` replaces the whole comp.** Generated comps must emit their own MediaIn/MediaOut (`FUSION-LANE.md` §5).
- **One fusionscript client at a time** (`AGENTS.md`). Reactor Standalone talks to Fusion too — do not run it while a pipeline script holds the connection.
- **Third-party OFX IDs: never guess.** Install, relaunch, dump `GetRegList(CT_Tool)` (or read `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/OFXPluginCacheV2.xml`), use the exact string. The spektrafilm session already paid for guessing enum indices.
- **User-dir OFX needs `OFX_PLUGIN_PATH`** and launching the binary directly; `open -a` drops the environment.
- **Unsigned OFX** (purzos, lenscorrect) need `xattr -dr com.apple.quarantine`.
- **Vonk / Reactor on 21.1 is inferred**, not stated. One node, one render, before building on it.
- **Colour-page plugins are not automatable.** A purchase intended for the pipeline must register in Fusion; verify with the dump before paying.
- The OFX research pass **launched Resolve on this machine** to run the registry dump; it was no longer running about twenty minutes later (quit or crash, not investigated). Nothing was saved or modified.

---

## 7. What happens next without a verdict (sequenced, each with its own done-criterion)

1. **Store claims** — written this session: the `ofx.` ID rule as a measured verdict; the scripting boundary (no Color-page OFX, no timeline keyframes) as a verdict; Krokodove-is-built-in and the MotionVFX acquisition as references. Done when `check-knowledge.py` and `check-retrieval.py` pass.
2. **prior-art.json rows** for the capability classes this survey covered (title/transition packs, Fusion package manager, retro/VHS/glitch effects, audio-reactive parameters, gyro stabilisation, film emulation additions). Done when the file lists them.
3. **`SetLUT` with a `.dctl` path** — one-line test next time Resolve is open. Done when the result is a claim.
4. **Reactor Standalone + one Vonk node on 21.1** — install, `vJSONFromFile` → a Text+ value, render one frame. Done when the frame shows the JSON value. This is the gate for the whole data-driven Fusion route.
5. **Gyroflow OFX on one Osmo ride clip** — user-dir install like spektrafilm, dump its ID, render 10 s against the same clip with RockSteady only. Done when a side-by-side sits in `jobs/…/evidence/` and Ryan has looked at it.
6. **purzos-ofx + ntsc-rs** — install, dump IDs, one contact sheet of five looks on a ride clip. Done when the sheet exists.
7. **OpenDRT** into `grades/film-look/manifest.json` and onto the open film-emulator comparison sheet (`compare-other-free-film-emulators-on-osmo-d-log-`).

Steps 4–7 write a Fuse, an OFX or a DCTL into Resolve's folders and render; they do
not change any project code.

---

## 8. Verdicts that are Ryan's — money, and one architecture call

Each is a genuine either/or: picking one means the other is not bought.

1. **Film emulation, paid or not.** (a) Stay free — Film Look Creator + print LUTs + spektrafilm once its parameters are read back, + OpenDRT on the comparison sheet. (b) FilmConvert Nitrate, $119. (c) Filmbox Looks, $199, after its 14-day trial. My read: (a) until the open comparison sheet has been looked at; the store already says the print LUT beat FLC on the 126 s frame and exposure discipline beats all of them.
2. **A template subscription, or none.** (a) None — 134 stock titles plus the Reactor atoms plus our own compiler. (b) Envato Elements Core at $16.50/mo for a month, download a shortlist, cancel. My read: (b) for one month, because the compiler's look pass would benefit from studying twenty polished `.setting` files, and one month is $16.50.
3. **Neat Video Pro for Resolve, $159.90, or Studio's own NR.** Only decidable after the open bookmark `denoise-high-iso-osmo-footage…` renders both on clip 0004. Not yet.
