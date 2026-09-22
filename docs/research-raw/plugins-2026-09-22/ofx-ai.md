# Third-party OFX effects and AI-assist tools for DaVinci Resolve Studio 21 on Apple Silicon (research, 2026-09-22)

Scope: a solo creator making stylised explainers, DJI Osmo Action 5 Pro ride footage, iPhone Apple Log footage and music-driven cuts, on DaVinci Resolve Studio 21.1.0 / Apple Silicon Mac.

Column key (same in every table): **Name | Maker | URL | Format | Price/licence (2026) | Resolve 20/21 + Apple Silicon as stated | Scriptable via Resolve Python API? | Why a solo creator wants it | Caveat**

Legend: VERIFIED = read on the vendor/primary page or measured on this machine. UNVERIFIED = only seen in a search summary, a reseller blurb, or a dated review.

---

## 0. Machine facts measured on this Mac (primary evidence, 2026-09-22)

| Fact | Value | How measured |
|---|---|---|
| Resolve 21.1 platform requirement | macOS 15 Sequoia + **Apple Silicon only** (Intel Macs dropped) — UNVERIFIED (third-party requirements pages, not BMD's). If true, any OFX without an arm64 slice (Intel-only or Rosetta-dependent builds) is a hard fail, not a caveat | search summaries |
| Resolve installed | DaVinci Resolve **21.1.0** (`/Applications/DaVinci Resolve/DaVinci Resolve.app`) | `defaults read .../Info.plist CFBundleShortVersionString` |
| Third-party OFX installed | **none** — `/Library/OFX/Plugins` does not exist | `ls /Library/OFX/Plugins` |
| OFX cache | `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/OFXPluginCacheV2.xml` is an empty `<cache version="ResolveHostV1">` | `cat` |
| OFX tools visible to Fusion | **101** registry entries with IDs starting `ofx.` (100 ResolveFX + 1 `ofx.com.blackmagicdesign.openfx.ColorGeneratorPlugin`) | `fuscript -l lua` → `resolve:Fusion():GetRegList(CT_Tool)` |
| `comp:AddTool("ofx.com.blackmagicdesign.resolvefx.Glow")` | returns a live tool `Glow1` with `ID = ofx.com.blackmagicdesign.resolvefx.Glow` | same script, hidden comp via `fu:NewComp(false,false)` |
| `comp:AddTool("ofx.com.blackmagicdesign.resolvefx.HalationPlugin")` | returns `Halation1` | same |
| Where the `ofx.` prefix rule lives | string `ofx.com.blackmagicdesign.resolvefx.` inside `.../Contents/Libraries/Fusion/Plugins/openfx.plugin` (universal x86_64+arm64 binary) and Lua in `libfusionsystem.dylib`: `id:sub(1,35) == "ofx.com.blackmagicdesign.resolvefx."` | `strings` |
| Resolve was launched by this research session for the registry test; it was no longer running ~20 min later (quit or crashed — not investigated) | — | `open -a "DaVinci Resolve"`, later `ps aux` showed no process |

---

## 1. The big OFX suites

| Name | Maker | URL | Format | Price / licence (2026) | Resolve 20/21 + Apple Silicon | Scriptable (Python API)? | Why a solo creator wants it | Caveat |
|---|---|---|---|---|---|---|---|---|
| Continuum 2026.5 | Boris FX | https://borisfx.com/products/continuum/ · hosts: https://borisfx.com/products/continuum/supported-hosts/ | OFX (Edit/Color/Fusion pages) | VERIFIED range: perpetual $365–$2,195 by host; subs $32–$112/mo, $215–$765/yr (CG Channel). OFX-only tier price: UNVERIFIED (Toolfarm page returned 403) | VERIFIED: hosts page lists "Blackmagic Davinci Resolve 21" and "20"; macOS 12–26 (Tahoe). Apple Silicon not called out on that page. Continuum 2025 news: "Continuum now supports Davinci Resolve's Fusion page" (the older BCC-in-Resolve doc page still says Fusion page NOT supported — stale) | YES in the Fusion page once installed: `comp.AddTool("ofx.<Continuum plugin identifier>")` — identifier discoverable with the Lua/Python registry dump in §6 (vendor prefix not verified here). Color-page instances: no API | Biggest single toolbox: Particle Illusion, Beat Reactor (audio-reactive — music-driven cuts), Video Glitch, Light Leaks, Scanline, Cartoon Look, Film Damage, Primatte keyer, Mocha tracking inside effects | Heavy and expensive; many effects are GPU-hungry; only two Resolve hosts named so check the matrix each major release |
| Sapphire 2026.5 | Boris FX | https://borisfx.com/products/sapphire/ | OFX | VERIFIED (CG Channel): perpetual $1,865 (Adobe/OFX ed.), $3,075 multi-host; sub $80/mo or $545/yr single; $144/mo or $985/yr multi | Hosts: After Effects, DaVinci Resolve, Flame, Nuke, Vegas, Fusion Studio on Win/Linux/macOS (CG Channel + borisfx docs). Explicit "Resolve 21" and Apple Silicon: UNVERIFIED on pages fetched. Fusion-page-inside-Resolve support: UNVERIFIED (host list names "DaVinci Resolve" and "Fusion Studio" separately) | Same as Continuum: YES in Fusion via `ofx.` id once installed; not on Color page | S_Glow, S_LensFlare + Flare Designer, S_FilmEffect, S_TVDamage, S_Cartoon / S_CartoonPaint, S_HalfTone, new S_AdvancedDefocus (bokeh, cat's-eye, lens dirt) — the "expensive glow" everyone imitates | Price is enterprise-grade for a solo creator; rent monthly for a project rather than buy |
| Mocha Pro 2026 | Boris FX | https://borisfx.com/products/mocha-pro/ | OFX plugin (Resolve Fusion page / Color page) or standalone | VERIFIED (CG Channel): perpetual $765 OFX plugin / $1,095 all plugins / $1,645 standalone+plugins; sub $48/mo or $325/yr OFX plugin | "OFX plugin compatible with DaVinci Resolve and Fusion Studio 18+"; "updated support for latest Apple silicon" (CG Channel). Resolve 21 explicit: UNVERIFIED | YES (Fusion page) via `ofx.` id; the Mocha UI itself is interactive, so scripting only places the node | Planar tracking + Matte Refine ML for screen inserts, sign replacement, object removal on ride footage | Overkill unless you do compositing weekly; Resolve's own Magic Mask 2 and Surface Tracker cover the easy cases free |
| Silhouette 2026 | Boris FX | https://borisfx.com/products/silhouette/ | OFX plugin or standalone | VERIFIED (CG Channel): plugin perpetual $1,195; $103/mo or $545/yr; standalone $2,195 | "available as a plugin for OFX-compatible apps like DaVinci Resolve". Resolve 21 / Apple Silicon explicit: UNVERIFIED | YES in Fusion via `ofx.` id (interactive UI inside) | Roto + paint at feature-film level | Not a solo-creator tool; listed for completeness |
| Red Giant 2026.5 (Magic Bullet, Trapcode, VFX, Universe) | Maxon | https://www.maxon.net/en/red-giant · KB: https://support.maxon.net/hc/en-us/articles/23987275556764-Red-Giant-Compatibility | OFX for the Resolve-compatible subset | VERIFIED (CG Channel): Red Giant complete $85/mo or $639/yr (includes Universe); Universe alone $32/mo or $214/yr. Maxon One $1,199/yr or $149/mo (B&H/Toolfarm/vfxer, UNVERIFIED on maxon.net) | Search summaries of the Maxon KB (page blocked by Cloudflare, could not fetch) say Red Giant/Universe support **Resolve 19 and 20**; **no page seen names Resolve 21** as of the 2026.5.1 (Aug 12 2026) notes. macOS 14.0+. Named as working in Resolve: Magic Bullet Looks, Shine, StarGlow (CG Channel), Universe. Trapcode Particular/Form and most of VFX Suite: After Effects-only — per-tool matrix is on the blocked KB page (UNVERIFIED) | YES for whichever ship as OFX filters, via `ofx.` id in Fusion; Universe generators also appear as Edit-page generators → `timeline.InsertOFXGeneratorIntoTimeline(name)` (name UNVERIFIED) | Magic Bullet Looks (one-click looks), Universe's Stylize category ("vintage, glitchy… retro and modern looks"), Real Lens Flares | Subscription only; Resolve 21 not on the stated list; Universe once had a "major bug" thread on the BMD forum for OFX. Treat as "works but a version behind" |
| Universe 2026 (standalone sub) | Maxon | https://www.maxon.net/en/red-giant/universe | OFX | $32/mo or $214/yr (VERIFIED CG Channel) | As above: Resolve 19/20 stated (UNVERIFIED), 2026.0 added Resolve on-screen gizmos and Fractal Background as a filter | As above | Cheapest way into the VHS/glitch/retro/HUD family with real presets | Rented, not owned |
| NewBlue TotalFX / Filters / Titler | NewBlue | https://newbluefx.com/resolve-plugins/ | OFX | Not captured; UNVERIFIED | Vendor: Resolve 15+; "Apple Silicon Mac support currently available via Rosetta, full native… soon" (search summary, UNVERIFIED date). BMD forum thread on DRS19 conflicts | Presumably YES via `ofx.` id; UNVERIFIED | Cheap titling and colour filters | Rosetta-only status and a history of breaking on Resolve majors — do not buy without a trial on 21.1 |
| Frischluft Lenscare OFX (DoF / Out-of-Focus) | Frischluft | https://frischluft.com/frischluft/ · https://www.toolfarm.com/buy/frischluft_lenscare_ofx/ | OFX | ~$227 (Novedge listing, UNVERIFIED) | Apple Silicon since May 2022; updated Feb 14 2025 (frischluft news). Reseller blurb says "Fusion 17 standalone, not Fusion inside Resolve" — UNVERIFIED for Resolve 21 | If it loads in the Fusion page: YES via `ofx.` id | Depth-of-field from Resolve's AI Depth Map → real bokeh | Small vendor, old-style licensing; test the demo on 21.1 before paying |
| RE:Vision Effects (Twixtor, ReelSmart Motion Blur, DE:Noise) | RE:Vision | https://revisionfx.com/products/for/resolve | OFX | Not captured; UNVERIFIED | Listed for Resolve in awesome-davinci-resolve; version/Apple Silicon UNVERIFIED | YES via `ofx.` id (Fusion) | Twixtor slow-mo on 60/120fps Osmo clips is still better than Optical Flow in some cases | Resolve 21 SpeedWarp (now a Fusion tool `SPDw`) + "2x faster Speed Warp Metal" narrows the gap |
| Neat Video | ABSoft | http://www.neatvideo.com/overview.html | OFX | Not captured; UNVERIFIED | Listed for Resolve (awesome list); UNVERIFIED for 21 | YES via `ofx.` id | Best-in-class temporal denoise for low-light iPhone Log | Resolve Studio's UltraNR (AI) is free with Studio — try it first |

---

## 2. Stylisation & look plugins

### 2a. Built-in ResolveFX you already own (Studio) — verified IDs from the live registry on this Mac

These compete directly with Universe/Continuum for a stylised-video creator and are the only ones with **verified** `AddTool` IDs. Studio-vs-free status per effect: UNVERIFIED (not checked).

| Effect (UI name) | Verified Fusion tool ID (`comp.AddTool(...)`) | Use |
|---|---|---|
| AI Stylize | `ofx.com.blackmagicdesign.resolvefx.Stylize` | the "anime / comic / painterly" ask, no third party needed |
| AI Cinematic Haze | `ofx.com.blackmagicdesign.resolvefx.CinematicHaze` | depth-aware atmosphere |
| AI CineFocus | `ofx.com.blackmagicdesign.resolvefx.CineFocus` | fake shallow DoF on action-cam footage |
| AI Depth Map | `ofx.com.blackmagicdesign.resolvefx.DepthMap` | feeds blur/haze/relight |
| AI Relight | `ofx.com.blackmagicdesign.resolvefx.Relight` | |
| AI UltraSharpen / AI Motion Deblur / AI Blemish Removal | `...UltraSharpen` / `...MotionDeblur` / `...BlemishRemoval` | new in 21 |
| Halation | `ofx.com.blackmagicdesign.resolvefx.HalationPlugin` | verified AddTool |
| Glow | `ofx.com.blackmagicdesign.resolvefx.Glow` | verified AddTool |
| Film Look Creator | `ofx.com.blackmagicdesign.resolvefx.FilmLook` | 21 adds Aurora preset + fade rolloff |
| Film Grain / Film Damage / Analog Damage / JPEG Damage | `...FilmGrain` / `...FilmDamage` / `...AnalogDamage` / `...JPEGDamage` | VHS/retro without a plugin |
| Scanlines | `ofx.com.blackmagicdesign.resolvefx.ScanlineV2` | |
| Lens Flare / Lens Reflections / Light Rays / Aperture Diffraction | `...LensFlareV2` / `...LensReflections` / `...Lightray` / `...ApertureDiffraction` | anamorphic-ish flares |
| Pencil Sketch / Watercolor / Abstraction / Emboss / Edge Detect | `...Sketch` / `...Watercolor` / `...Abstraction` / `...Emboss` / `...EdgeDetect` | classic stylise |
| Stop Motion / Motion Trails / Camera Shake / Video Collage / Picture In Picture | `...StopMotion` / `...MotionTrails` / `...CameraShake` / `...VideoCollage` / `...PictureInPicture` | explainer energy |
| ColorTone Diffuser / Prism Blur / Tilt-Shift Blur / Lens Distortion / Chromatic Aberration Removal | `...ColorToneDiffuser` / `...PrismBlur` / `...TiltShiftBlur` / `...LensDistortion` / `...ChromaticAberration` | |
| Surface Tracker / Patch Replacer / Beauty / Dehaze / Deflicker / Deband / DCTL | `...SurfaceTracker` / `...PatchReplacer` / `...Beauty` / `...Dehaze` / `...Deflicker` / `...Deband` / `...DCTL` | utilities |

Full list of all 101 IDs: **Appendix A** at the end of this document (measured on this Mac; regenerate with the §6 Lua snippet).

### 2b. Third-party stylisation / look plugins

| Name | Maker | URL | Format | Price / licence (2026) | Resolve 20/21 + Apple Silicon | Scriptable? | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| Dehancer Pro 7.4.1 (film emulation, grain, halation, bloom, film damage) | Dehancer | https://www.dehancer.com/shop/davinci_resolve/pro | OFX | Feb 2025 review (theotivity): perpetual Pro $449, Lite $199, add-on packs (Bloom/Grain/Breath/Halation) $99 each. Dehancer FAQ says plans have changed and now references Subscription/Studio/Production plans — **2026 pricing UNVERIFIED** (page is JS-rendered) | VERIFIED vendor page: macOS 13+, "Resolve 19 or newer", Metal GPU; "optimized for Apple Silicon"; v7.4.1 released 30 Jun 2026 | YES in Fusion via `ofx.` id once installed (identifier UNVERIFIED); normally used on the Color page → not scriptable there | The most complete "make it look like film" box: 60+ stocks, print, halation, bloom, gate weave | Grain+Halation+Bloom "tank your frame rate" on 4K (thebytelab, Jun 2026); disable while grading, enable for render |
| Filmbox Pro / Filmbox Looks | Video Village | https://videovillage.com/filmbox/buy | OFX | VERIFIED: Looks $29/qtr, $69/yr, $199 perpetual; Pro $129/qtr, $349/yr, $999 perpetual; sub payments credit toward perpetual; 14-day trial | macOS 12+; hosts include DaVinci Resolve (version not stated); Apple Silicon not explicitly stated | As Dehancer | Colourist-grade negative+print emulation with per-parameter halation/grain/acutance; Looks tier is the solo-creator price point | Pro is $999; Looks is the sensible buy |
| Scatter (diffusion emulation) | Video Village | https://videovillage.com/scatter/buy | OFX | VERIFIED: $99/qtr, $199/yr, $499 perpetual; 14-day trial; 2 activations | macOS 12+; hosts include Resolve | As above | Physically modelled Pro-Mist/Black-Mist style bloom and halation — the "cinematic" softness on iPhone Log | Resolve's own ColorTone Diffuser + Halation cover 70% of this free |
| FilmConvert Nitrate (OFX) | FilmConvert | https://www.filmconvert.com/purchase | OFX | VERIFIED: $119 (RRP $149) Resolve plugin; $179 (RRP $225) all-host bundle | Resolve support stated; version/Apple Silicon UNVERIFIED | As above | Cheapest reputable film stock + grain + halation with camera profiles (iPhone/DJI profiles: UNVERIFIED) | Camera profile coverage for Osmo Action 5 Pro not checked |
| CineMatch | FilmConvert | https://www.cinematch.com | OFX | $259 per host (ProVideo Coalition, UNVERIFIED for 2026) | Resolve + Premiere; UNVERIFIED for 21 | As above | Matches iPhone Apple Log to DJI D-Log M scientifically — exactly this creator's two-camera problem | Resolve Colour Management + CST does the basic version free |
| Universe Stylize category (VHS, glitch, retro, HUD etc.) | Maxon | https://www.maxon.net/en/red-giant/universe | OFX | $32/mo or $214/yr (VERIFIED) | Resolve 19/20 stated (UNVERIFIED), 21 not stated | YES (Fusion) via `ofx.` id | Preset-driven retro looks with the most presets of any option | Individual tool names not captured from maxon.net (JS page) — UNVERIFIED list |
| Continuum "Distort & Stylize" / "Film Looks & Grain" / "Light & Diffusion" | Boris FX | https://borisfx.com/products/continuum/ | OFX | See §1 | See §1 | YES (Fusion) | Cartoon Look (https://borisfx.com/effects/continuum-cartooner), Video Glitch, Light Leaks, Scanline, Film Damage, Halftone, Posterize | Unit-level pricing page returned 404; individual units exist but prices UNVERIFIED |
| Sapphire Stylize / Lighting | Boris FX | https://borisfx.com/documentation/sapphire/ofx/cartoon/ | OFX | See §1 | See §1 | YES (Fusion) | S_Cartoon, S_CartoonPaint, S_HalfTone, S_Etching, S_Glow, S_LensFlare | Price |
| purzOS OFX (64 free effects: ASCII, Bayer dither, pixel sort, CRT, VHS, datamosh, halation, bloom, duotone, kaleidoscope…) | purzbeats (Purz) | https://github.com/purzbeats/purzos-ofx | OFX, MIT | Free | VERIFIED: v0.2.0 (2026-07-10) ships `purzos-ofx-macos-arm64.zip`; "tested in DaVinci Resolve and Natron"; unsigned → `xattr -dr com.apple.quarantine /Library/OFX/Plugins` | YES in Fusion via `ofx.<identifier>` (identifier not documented; dump the registry after install) | The best free retro/glitch set for music-driven cuts; deterministic (seeded) so renders are reproducible | Unsigned, one-developer project, Resolve version tested not stated |
| ntsc-rs (NTSC/VHS signal emulation) | ntsc-rs (valadaptive) | https://ntsc.rs/docs/openfx-plugin/ · https://github.com/ntsc-rs/ntsc-rs/releases | OFX (+ AE + standalone), open source | Free | VERIFIED: v0.9.6 (2026-09-05) ships `ntsc-rs-macos-openfx.pkg`; docs: "works perfectly in Resolve's Color and Fusion pages"; installs to `/Library/OFX/Plugins/`; note "Apply sRGB gamma" toggle because Resolve hands it sRGB | YES (Fusion) via `ofx.` id | The most authentic free VHS/composite look; category "Filter" | Apply in Fusion (pre-scale) or in a matching-res timeline, per its docs; the `~/.ofx/plugins` path in its docs is nonstandard for Resolve — untested |
| VHS Nostalgia | xere.my | https://xere.my/store/vhs-nostalgia/ | OFX | €49 (VERIFIED xere.my comparison) | macOS+Windows, Free & Studio; "rebuilds the NTSC composite signal line by line"; Resolve 21 explicit UNVERIFIED | YES via `ofx.` id (UNVERIFIED id) | Real-time playback at HD/4K | Small vendor |
| Phosphor (CRT + VHS emulation, 21 device presets) | PixelTools | https://pixeltoolspost.com/products/phosphor | OFX (Edit + Color pages) | VERIFIED: $99.99 one-time | VERIFIED: Studio required; macOS Metal, Apple Silicon supported; ACES/DWG scene-referred | Edit/Color only per vendor → not scriptable unless it also registers in Fusion (UNVERIFIED) | Physically modelled composite→tape→display chain; colour-managed | Studio only; $100 vs free ntsc-rs |
| Camcorder / CRT Machine / Mixed Media | BLEWTOOF | https://blewtoof.mov | OFX | Camcorder $32 (xere.my) | Studio only; macOS+Windows | UNVERIFIED | Date-stamp camcorder look with fonts | Studio only |
| Akascape Fuses (Super VHS, Datamosh, Super Glitch, Pixel Sorting, CRT, ASCII, SupaScale anime upscaler, Neural Style Transfer, RemBG, RemObj) | Akascape | https://www.akascape.com | Fusion **Fuse** (not OFX) | Free/open source for many; SuperVHS $25 (xere.my) | Free & Studio, macOS/Win/Linux; several AI ones need external Python deps | YES — Fuses are native Fusion tools: `comp.AddTool("<FuseName>")` | Broadest free "trendy" effect set; Neural Style Transfer + SupaScale answer the anime ask | Fuses run on CPU/Lua+GPU shader — slower than OFX; AI fuses need setup |
| boilify (line-boil / hand-drawn jitter) | Microck | https://github.com/Microck/boilify | OFX | Free | Repo pushed 2026-07-15; "Resolve Studio 20+" per awesome list; arm64 build UNVERIFIED | YES via `ofx.` id | Comic/animated-explainer wobble | Early project |
| AnamorphicTool (AnamorphicUtility + AnamorphicFX) | independent dev "Bruce" | https://anamorphictool.com/ | OFX | UNVERIFIED (site 403); trial available | Resolve-only, launched 2026-03-18 (CineD); Apple Silicon UNVERIFIED | UNVERIFIED | AnamorphicFX = anamorphic squeeze/flare/vintage character on any footage | Brand-new, one developer |
| lenscorrect-ofx (Lensfun-based distortion/vignette/CA correction) | murtazatunio | https://github.com/murtazatunio/lenscorrect-ofx | OFX, MIT | Free | VERIFIED: **Apple Silicon macOS 12+ only** (Windows planned); v0.1.0; installs `lenscorrect-ofx.ofx.bundle` to `/Library/OFX/Plugins/` | YES via `ofx.` id | Lensfun profiles — the "Lensfun-style" ask; potentially de-fish the Osmo Action wide lens | Early (0.1.0); Osmo Action 5 Pro profile presence in Lensfun DB UNVERIFIED |
| spektrafilm OFX (beta spectral film emulation) | spektrafilm | https://spektrafilm.114c.de | OFX | Free beta | UNVERIFIED | UNVERIFIED | Negative/print/scan stages, free | Beta |
| Cartoon / anime via Resolve AI Stylize | Blackmagic | built-in | ResolveFX | included with Studio | 21.1 verified present | **YES** `ofx.com.blackmagicdesign.resolvefx.Stylize` (verified id) | no third-party purchase needed for painterly/comic | AI look; consistency frame-to-frame not evaluated |

---

## 3. AI tools that plug into Resolve

### 3a. Resolve 20/21's own AI features (Studio unless noted; UNVERIFIED which few are in the free tier)

Source: Resolve 21 New Features Guide PDF (April 2026) table of contents (read directly), Larry Jordan's Resolve 20 list, Broadcast/VP Land coverage.

| Version | Feature | What it does | Scriptable? |
|---|---|---|---|
| 21 | AI IntelliSearch | search people/objects/dialogue across media | no API seen |
| 21 | AI Speech Generator | text-to-speech voices inside Resolve (ElevenLabs-style, built in) | no API seen |
| 21 | AI CineFocus | fake rack focus / shallow DoF | ResolveFX `…CineFocus` (verified id) |
| 21 | AI Face Age Transformer / AI Face Reshaper | face retouch | UNVERIFIED id |
| 21 | AI Blemish Removal | ResolveFX `…BlemishRemoval` (verified id) | yes (Fusion) |
| 21 | AI Slate Finder / Slate ID | logging | n/a |
| 21 | AI UltraSharpen / AI Motion DeBlur | ResolveFX `…UltraSharpen`, `…MotionDeblur` (verified ids) | yes (Fusion) |
| 21 | Photo page; Krokodove toolset integrated into Fusion; OpenFX 1.5 colour-management APIs for colour-space-aware effects; Fusion animation driven by Fairlight audio; SpeedWarp as Fusion tool; Lottie + OGraf HTML support | new surfaces | Fusion tools are scriptable |
| 20 | AI IntelliScript (now with Final Draft import in 21) | builds a timeline from a script | no API seen |
| 20 | AI Animated Subtitles | word-highlight subtitles | no API seen |
| 20 | AI IntelliCut | silence removal, per-speaker split, ADR cues | no API seen |
| 20 | AI Magic Mask 2 (+ paint brush; 21 can render it as external matte) | segmentation/tracking | Color page; no API |
| 20 | AI VoiceConvert (user-trainable) / AI Dialogue Matcher / AI Audio Assistant / AI Music Editor / AI Beat Markers (Detect Music Beats) | Fairlight | no API seen |
| 20 | AI Multicam SmartSwitch, AI Set Extender, AI SuperScale 3x/4x, AI Depth Map 2, UltraNR, IntelliTrack | — | Depth Map = ResolveFX `…DepthMap` (verified id) |

### 3b. Third-party AI tools

| Name | Maker | URL | Format | Price / licence (2026) | Resolve 20/21 + Apple Silicon | Scriptable? | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| AutoSubs v3.10.1 | Tom Moroney (tmoroney) | https://github.com/tmoroney/auto-subs · https://tom-moroney.com/auto-subs/ | Standalone app that drives Resolve via the scripting API (+ Premiere/AE CEP) | Free, MIT | VERIFIED: release 2026-09-19 ships `AutoSubs-Mac-ARM.pkg` / `macos-aarch64`; on-device Whisper, diarisation, translation, SRT or direct-to-Resolve | It IS a script client; the underlying transcription/subtitle placement can be reproduced in your own Python | Best free captions path; runs local, no cloud | External scripting (which AutoSubs uses) needs Studio; Free Resolve only runs scripts from its internal console — UNVERIFIED whether the app documents this |
| StoryToolkitAI v0.25.1 | octimot | https://github.com/octimot/StoryToolkitAI | Python app + Resolve API integration | Free, GPL-3.0 | Last release 2025-02-20, repo still pushed 2026-07-28; "Resolve Studio 18 integration via API"; Whisper + semantic search + ChatGPT | Python; integrates through the same API | Semantic search across transcripts, auto-markers, translation | Slower cadence than AutoSubs; Studio required |
| Topaz Video (formerly Video AI) — OFX plugin | Topaz Labs | https://docs.topazlabs.com/topaz-video/plugins | Standalone + **OFX plugin** (Enhance + Interpolation only) | VERIFIED (videoproc, Aug 2026): Personal $299/yr ($59 month-to-month); Pro $699/yr; Topaz Studio $399/yr | VERIFIED docs: "DaVinci Resolve Studio is required, free version will not load"; installs to `/Library/OFX/Plugins`; Apple Silicon supported (Starlight Mini wants 36 GB unified) | YES in Fusion via `ofx.` id (UNVERIFIED id) if the plugin registers there — docs describe Edit/Color usage | Upscale/deinterlace/deblur old or 1080p clips; slow-mo interpolation | Subscription; heavy GPU; Resolve's SuperScale/UltraSharpen are free with Studio |
| Colourlab AI 4 (Creator / Pro) | Colourlab | https://colourlab.ai/pricing/ · https://4.colourlab.ai/ | Standalone app that round-trips with Resolve via **OpenTimelineIO** (older v3: DaVinci sync + Look Designer OFX) | VERIFIED pricing page: Creator 3 $15/mo, $150/yr, $299 perpetual; Look Designer 3 for Resolve $24/mo, $249/yr, $490 perpetual. v4: "free during public beta… new build every 14 days through September" (year not stated on page — ambiguous today, 2026-09-22) | VERIFIED: v4 "Requires an Apple Silicon Mac — Windows support coming in October" | The app itself is not scriptable; Look Designer OFX would be via `ofx.` id (UNVERIFIED) | Auto shot-matching iPhone Log vs DJI vs stock B-roll; "every look starts with a word" prompt grading | Subscription creep; v4 beta churn |
| CorridorKey-Runtime (native AI keying OFX) | Alexandre Alvaro | https://github.com/alexandremendoncaalvaro/CorridorKey-Runtime | OFX | Free | Repo pushed 2026-08-05, 751 stars; arm64 build UNVERIFIED | YES via `ofx.` id | AI green-screen-free keying for talking-head explainers | Early project |
| Rembg-Fuse / RemObj-Fuse / Super-Style-Transfer-Fuse / SupaScale | Akascape | https://github.com/Akascape/Rembg-Fuse | Fusion Fuses calling external Python (rembg, LaMa, style-transfer) | Free | Needs local Python env; macOS supported per repo (UNVERIFIED arm64 specifics) | YES — Fuses are `comp.AddTool` targets | Background removal, object removal, anime style transfer inside Fusion | Setup friction; slow |
| Gyroflow OpenFX v2.1.1 | Gyroflow | https://docs.gyroflow.xyz/app/video-editor-plugins/davinci-resolve-openfx · https://github.com/gyroflow/gyroflow-plugins/releases | OFX | Free, open source | VERIFIED: `Gyroflow-OpenFX-macos.dmg` (2025-08-24); Metal on Mac; works in Free and Studio, but "Load for current file" auto-detect needs Studio; install to `/Library/OFX/Plugins`; Osmo Action 4/5 gyro supported by the Gyroflow app | YES via `ofx.` id (UNVERIFIED id); the Gyroflow app itself has a CLI | Gyro-data stabilisation for the Osmo Action 5 Pro that beats Resolve's stabiliser and RockSteady crops | Timeline fps must match source; plugin release is 13 months old (still current per repo) |
| ElevenLabs | ElevenLabs | https://elevenlabs.io | Web/API only — no Resolve plugin found | Usage tiers (not captured) | n/a | Their REST API is scriptable from your own Python → import WAV via Resolve API | Voice-over for explainers | Resolve 21 now has its own AI Speech Generator and VoiceConvert; no native bridge exists |
| Runway / Luma | Runway, Luma | — | No Resolve plugin/bridge found in any search | — | — | Their APIs are scriptable; drop renders into the Media Pool via `MediaStorage.AddItemListToMediaPool` | Generative B-roll | UNVERIFIED that any first-party Resolve bridge exists in 2026 — treat as none |
| "Generative fill" for Resolve | Blackmagic | built-in | AI Set Extender (Resolve 20) is the in-app equivalent | Studio | verified feature list | no API seen | Extend frames for 9:16 reframes | Quality untested here |
| Jumper / Tagger / arkiv / metafootage / BadWords / FireCut / AutoCut | various | see awesome-davinci-resolve | Scripts/panels using the Resolve API | Mixed (BadWords, arkiv, metafootage free) | UNVERIFIED individually | They are API clients | Footage search, auto-tagging, silence cutting | Not evaluated |

---

## 4. Audio-side plugins for Fairlight (brief)

| Name | Maker | URL | Format | Price (2026) | Resolve/Apple Silicon | Scriptable? | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| iZotope RX 12 (Elements / Standard / Advanced) | iZotope (Native Instruments) | https://www.izotope.com/en/products/rx.html | AU/VST3 (+ standalone editor) | VERIFIED (musictech/mixinggpt summaries): Elements $99, Standard $399, Advanced $1,399 | Spec page officially lists **Resolve 19** (lag vs. real incompatibility unknown); ARA only in Logic/Studio One — no ARA in Fairlight | Fairlight FX are not exposed to the Python API | Dialogue de-noise/de-reverb/de-click for ride audio | Fairlight's own Dialogue Separator + Voice Isolation cover the basics |
| Accentize dxRevive / dxRevive Pro | Accentize | https://www.accentize.com/product/dxrevive/ | VST3/AU/AAX | $99 / $299 (kvraudio/reseller, UNVERIFIED) | Vendor: "Apple Silicon recommended"; used in Resolve per fxfactory listing | no | One-knob dialogue restoration that often beats RX for speed | — |
| Waves Clarity Vx / Vx Pro / DeReverb Pro | Waves | https://www.waves.com/plugins/clarity-vx | VST3/AU | $39.99 / $199.99 / $119 (equipboard, UNVERIFIED) | "works in Resolve though official support limited to DAWs" (search summary) | no | Cheap real-time voice noise reduction | Waves Update Plan licensing |

---

## 5. Free / open-source OFX plugins — do they load in Resolve 21 on macOS arm64?

| Name | Maker | URL | Format | Licence | Loads in Resolve 21 / arm64? | Scriptable? | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| purzos-ofx | purzbeats | https://github.com/purzbeats/purzos-ofx | OFX | MIT | **Ships arm64 macOS build** (v0.2.0, 2026-07-10), "tested in DaVinci Resolve"; specific 21.1 test UNVERIFIED — high confidence | YES (Fusion) | 64 retro/glitch effects | Unsigned: clear quarantine |
| ntsc-rs | ntsc-rs | https://ntsc.rs/docs/openfx-plugin/ | OFX | Open source | **Ships `ntsc-rs-macos-openfx.pkg`** (v0.9.6, 2026-09-05); docs say Color+Fusion pages work — high confidence | YES (Fusion) | VHS | sRGB toggle |
| Gyroflow OpenFX | Gyroflow | https://github.com/gyroflow/gyroflow-plugins | OFX | Open source | **Ships macOS dmg**, Metal; documented for Resolve — high confidence | YES (Fusion) | stabilisation | fps match |
| lenscorrect-ofx | murtazatunio | https://github.com/murtazatunio/lenscorrect-ofx | OFX | MIT | **Apple Silicon only**, macOS 12+, v0.1.0 | YES | Lensfun correction | early |
| boilify | Microck | https://github.com/Microck/boilify | OFX | open | "Resolve Studio 20+"; arm64 asset UNVERIFIED | YES | line boil | early |
| CorridorKey-Runtime | A. Alvaro | https://github.com/alexandremendoncaalvaro/CorridorKey-Runtime | OFX | open | UNVERIFIED arm64 | YES | AI keying | early |
| DMC-BaldavengerOFX-MacOSarm64 | Demystify-Color | https://github.com/Demystify-Color/DMC-BaldavengerOFX-MacOSarm64 | OFX | (Baldavenger licence) | "rebuilt as macOS universal binaries", pushed 2026-05-28 — UNVERIFIED on 21.1 | YES | Baldavenger grading tools (film-style curves, etc.) on Apple Silicon | Original BaldavengerPlugins repo (pushed 2021) is **Intel-only**; GitHub issue #4 (M1, 2021) unresolved |
| openfx-misc (NatronOFX) | NatronGitHub | https://github.com/NatronGitHub/openfx-misc | OFX | GPL | **Does not ship a loadable arm64 build.** Last release Natron-2.5.0 (Nov 2022) has no macOS-arm64 asset; README-hosts.txt proves historical Resolve 12.5/16 testing with many Resolve-specific workarounds; issue #54 (Windows, Resolve 15, plugins invisible) unresolved. Verdict: UNVERIFIED / likely no without building from source | if loaded, YES | Would give Transform, CornerPin, Grade, Merge-style basics | Build yourself, or skip — Resolve already has these natively |
| openfx-gmic (G'MIC OFX) | NatronGitHub / MrKepzie | https://github.com/NatronGitHub/openfx-gmic · https://discuss.pixls.us/t/gmic-for-openfx-and-adobe-plugins/452 | OFX | CeCILL/GPL | Repo pushed 2024-02-18; historical Resolve 15/16 users needed Info.plist hacks (CFBundleName etc.); no arm64 build seen. Verdict: UNVERIFIED / likely no | if loaded, YES | 500+ G'MIC filters (painterly, comic, halftone) | Rebuild required |
| TuttleOFX | tuttleofx | https://github.com/tuttleofx/TuttleOFX | OFX | open | **Dead**: last push 2020-08-13; never targeted Resolve/arm64. Verdict: no | — | — | skip |
| Akascape Fuses / Shaderfuse (nmbr73) | Akascape / nmbr73 | https://www.akascape.com · https://github.com/nmbr73/Shaderfuse | Fusion Fuse (Lua/DCTL shaders) | mostly free/open | Fuses are architecture-independent → load on arm64 (Shadertoy shaders converted) | YES (`comp.AddTool` by Fuse name) | Hundreds of free GPU effects | CPU/Lua overhead; some need Studio |
| Reactor (installer, see §6) | We Suck Less | https://gitlab.com/WeSuckLess/Reactor | Lua package manager | free | Resolve 15–20+ stated; runs in 21 UNVERIFIED (Lua, should) | it is itself a script | one-click install of Fuses/macros/scripts | community quality varies |

---

## 6. Plugin managers, where OFX lives, and the OFX tool id for `comp.AddTool` (primary evidence)

### Where OFX lives on macOS
- System-wide: `/Library/OFX/Plugins/<Name>.ofx.bundle/Contents/MacOS/<Name>.ofx` (root `/Library`, not `~/Library`). Confirmed by Gyroflow docs, ntsc-rs docs, Topaz docs, Dehancer README, and the string `/Library/OFX` inside Resolve's `openfx.plugin`.
- Alternative: any folder in `OFX_PLUGIN_PATH` (purzos README; OFX standard).
- Resolve's scan cache: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/OFXPluginCacheV2.xml` (empty on this Mac — zero third-party OFX installed). openfx-misc's notes name the old `/Library/Application Support/Blackmagic Design/DaVinci Resolve/OFXPluginCache.xml` and the OFX log at `.../DaVinci Resolve.app/Contents/Resources/ofxTestLog.txt`.
- Unsigned bundles need `xattr -dr com.apple.quarantine /Library/OFX/Plugins`.
- Mac App Store Resolve may not load third-party OFX (Dehancer README) — this Mac has the direct-download build.
- Fuses/macros/scripts live under `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/{Fuses,Templates,Scripts}` and the per-user equivalent (Resolve Scripting README).

### Plugin managers
| Name | URL | What |
|---|---|---|
| Reactor | https://gitlab.com/WeSuckLess/Reactor · https://kartaverse.github.io/Reactor-Docs/ | Free WSL package manager for Fusion/Resolve: drag `Reactor-Installer.lua` into a Fusion comp; installs Fuses, macros, scripts as "Atoms". Stated Resolve 15–20+; 21 UNVERIFIED |
| Gyroflow app "Video editor plugins" panel | https://docs.gyroflow.xyz/app/video-editor-plugins/davinci-resolve-openfx | Installs/updates its own OFX when it detects Resolve |
| FxFactory | https://fxfactory.com/products/applesilicon/davinciresolve/ | macOS plugin store/manager; lists Resolve-compatible Apple Silicon packs (e.g. dxRevive). Which packs are OFX vs. audio: UNVERIFIED |
| Toolfarm / Maxon App / Boris FX Hub | vendor installers | Boris and Maxon install via their own hubs |
| There is no first-party Blackmagic OFX manager; installation is file-drop + relaunch. |

### How an OFX effect is identified in Fusion scripting — VERIFIED on Resolve 21.1.0
Rule: **Fusion tool ID = `"ofx." + <OFX plugin identifier (kOfxPropPluginIdentifier)>`.**

Evidence:
1. `libfusionsystem.dylib` contains Lua: `if iconid:sub(-4):lower() == ".png" or id:sub(1,35) == "ofx.com.blackmagicdesign.resolvefx." then` — Fusion special-cases IDs with that prefix.
2. `Libraries/Fusion/Plugins/openfx.plugin` (universal x86_64+arm64) contains the strings `ofx.com.blackmagicdesign.resolvefx.`, `/Library/OFX`, `OfxPluginPropFilePath`.
3. Live registry dump (Resolve running, `fuscript -l lua`):

```lua
resolve = bmd.scriptapp("Resolve"); fu = resolve:Fusion()
for _, reg in ipairs(fu:GetRegList(CT_Tool)) do
  if reg.ID:sub(1,4) == "ofx." then print(reg.ID, "|", reg.Name) end
end
-- 101 hits on this Mac, e.g.
-- ofx.com.blackmagicdesign.resolvefx.Glow            | Glow
-- ofx.com.blackmagicdesign.resolvefx.HalationPlugin  | Halation
-- ofx.com.blackmagicdesign.resolvefx.Stylize         | AI Stylize
-- ofx.com.blackmagicdesign.openfx.ColorGeneratorPlugin | Color Generator
```
4. `comp:AddTool("ofx.com.blackmagicdesign.resolvefx.Glow", 0, 0)` → tool `Glow1`, `ID == "ofx.com.blackmagicdesign.resolvefx.Glow"`; same for `HalationPlugin` → `Halation1`. (Tested in a hidden `fu:NewComp(false,false)` comp; the production path is `timelineItem.GetFusionCompByIndex(1)` / `AddFusionComp()` then `.AddTool(...)`.)

Python equivalent (Studio, external script) — **UNTESTED**: the Lua form above is the verified one; Resolve had quit before this could be run. Only `comp.AddTool(id)` (verified in Lua) and `GetFusionCompByIndex` / `AddFusionComp` (from the .pyi) are certain; `fu.CT_Tool` and the shape of `GetRegList`'s Python return are guesses.
```python
# UNTESTED — see note above
import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve"); fu = resolve.Fusion()
ofx_ids = {r.ID: r.Name for r in fu.GetRegList(fu.CT_Tool if hasattr(fu,"CT_Tool") else 1).values() if str(r.ID).startswith("ofx.")}
item = resolve.GetProjectManager().GetCurrentProject().GetCurrentTimeline().GetCurrentVideoItem()
comp = item.GetFusionCompByIndex(1) or item.AddFusionComp()
glow = comp.AddTool("ofx.com.blackmagicdesign.resolvefx.Glow")
```
(`CT_Tool` constant access from Python: UNVERIFIED — the Lua form is verified; if the constant is not exposed, call `fu.GetRegList(1)` or iterate `fu:GetRegSummary()` via `resolve.Fusion().ExecuteLua` — UNVERIFIED.)

Third-party identifiers: **do not guess** `com.genarts.sapphire…`, `com.borisfx…`, `com.redgiant…` prefixes — none were verified here. Install the bundle, relaunch Resolve, run the dump above (or read `OFXPluginCacheV2.xml`), and use the exact string that appears.

### Scriptability boundary (from `Developer/Scripting/DaVinciResolveScript.pyi` on this Mac)
- Fusion page: full — `TimelineItem.AddFusionComp()`, `GetFusionCompByIndex/Name`, `ImportFusionComp`, `ExportFusionComp`, then the whole Fusion object model (`comp.AddTool`, `tool.SetInput`, etc.).
- Edit page: OFX **generators only** — `Timeline.InsertOFXGeneratorIntoTimeline(generatorName)`; also `InsertFusionGeneratorIntoTimeline`, `InsertFusionTitleIntoTimeline`, `AddTransition(TransitionOptions)` where transition category may be `'ofx'`.
- **No API exists to add an OFX filter to an Edit-page clip, to add an OFX node on the Color page, or to touch Fairlight FX.** A Color-page OFX (where Dehancer, Filmbox, Phosphor are normally used) is therefore not scriptable; put such effects in a Fusion comp instead if automation matters.
- Public docs mirrors: https://resolvedevdoc.readthedocs.io/en/latest/readme_resolveapi.html · https://deric.github.io/DaVinciResolve-API-Docs/ · https://wiki.dvresolve.com/developer-docs/scripting-api

---

## Top picks for this solo creator (Studio 21.1, Apple Silicon)

Start with what is already installed: the 101 ResolveFX are scriptable by verified ID and cover halation, glow, film look, analog/film/JPEG damage, scanlines, lens flare, AI Stylize (the anime/comic ask) and AI CineFocus — build the house style there first, because every one of them can be dropped into a Fusion comp by `comp.AddTool("ofx.com.blackmagicdesign.resolvefx.<X>")`. Add three free OFX that ship native arm64 builds today: **Gyroflow OpenFX** (gyro-true stabilisation for the Osmo Action 5 Pro — this is the single biggest quality win on ride footage), **purzos-ofx** (64 seeded, deterministic retro/glitch/dither effects for music-driven cuts) and **ntsc-rs** (the most convincing free VHS). If money goes anywhere, put it on one film-look plugin — **Filmbox Looks at $199 perpetual** or **FilmConvert Nitrate at $119** — rather than Dehancer's $449 (2026 pricing unverified) or a Boris/Maxon subscription; and use **AutoSubs** (free, arm64 pkg released three days ago) for captions before paying for anything. Rent Continuum or Universe by the month only for a specific job that needs Particle Illusion / Beat Reactor or a preset library; note Maxon's KB reportedly still lists Resolve 19/20, not 21 (UNVERIFIED — page blocked). Skip openfx-misc, G'MIC OFX and TuttleOFX: none ships an arm64 build that loads in Resolve 21 without you compiling it.

---

## Sources

Local evidence (this Mac, 2026-09-22)
- `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Info.plist` (21.1.0)
- `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/Plugins/openfx.plugin` (strings: `ofx.com.blackmagicdesign.resolvefx.`, `/Library/OFX`)
- `/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/libfusionsystem.dylib` (Lua prefix check)
- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/{README.md,DaVinciResolveScript.pyi}`
- `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/OpenFX/` (BMD OFX SDK samples: Gain, DissolveTransition, TemporalBlur, RandomFrameAccess; OpenFX-1.4 headers; Metal/CUDA/OpenCL kernels)
- `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/OFXPluginCacheV2.xml` (empty)
- Registry dump + AddTool test output: `/private/tmp/claude-501/-Users-SSDrive-projects-mediaStudio/b13169de-2321-49f8-a6b6-80b82037b2af/scratchpad/ofx_ids.txt`

Web
- https://www.cgchannel.com/2025/11/boris-fx-releases-continuum-2026/
- https://www.cgchannel.com/2026/05/boris-fx-releases-continuum-2026-5/
- https://borisfx.com/products/continuum/supported-hosts/
- https://borisfx.com/products/continuum/
- https://borisfx.com/news/continuum-2025/
- https://borisfx.com/documentation/continuum/bcc-overview-in-resolve/
- https://borisfx.com/effects/continuum-cartooner
- https://www.cgchannel.com/2025/11/boris-fx-releases-sapphire-2026/
- https://www.cgchannel.com/2026/05/boris-fx-releases-sapphire-2026-5/
- https://borisfx.com/products/sapphire/
- https://borisfx.com/documentation/sapphire/ofx/cartoon/
- https://borisfx.com/documentation/sapphire/ofx/general-info/
- https://support.borisfx.com/hc/en-us/articles/11038964353933-What-is-OFX
- https://www.cgchannel.com/2025/12/boris-fx-releases-mocha-pro-2026/
- https://borisfx.com/products/mocha-pro/
- https://mixinglight.com/color-grading-tutorials/mocha-pro-ofx-plugin-for-fusion/
- https://www.cgchannel.com/2026/05/boris-fx-releases-silhouette-2026/
- https://borisfx.com/products/silhouette/
- https://www.cgchannel.com/2025/09/maxon-releases-red-giant-2026-0-and-universe-2026-0/
- https://www.cgchannel.com/2026/07/maxon-releases-red-giant-2026-5/
- https://support.maxon.net/hc/en-us/articles/23987275556764-Red-Giant-Compatibility (blocked by Cloudflare; content via search summaries only)
- https://support.maxon.net/hc/en-us/articles/23369159655708-Universe-2026-0-0-September-10-2025 (403)
- https://support.maxon.net/hc/en-us/articles/13764887933596-Red-Giant-2026-5-1-August-12-2026
- https://www.maxon.net/en/red-giant/universe
- https://www.maxon.net/en/red-giant
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=145177 (Universe OFX bug thread)
- https://www.bhphotovideo.com/c/product/1594461-REG/maxon_mxo_y_one_annual_subscription.html
- https://www.toolfarm.com/buy/maxon_one/
- https://www.vfxer.com/maxon-one-price-coupon-codes/
- https://newbluefx.com/resolve-plugins/
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=207281 (NewBlue / DRS19 conflict)
- https://frischluft.com/frischluft/
- https://www.toolfarm.com/buy/frischluft_lenscare_ofx/
- https://novedge.com/products/buy-frischluft-lenscare-ofx
- https://forum.blackmagicdesign.com/viewtopic.php?f=32&t=90053 (Frischluft in Fusion inside Resolve)
- https://www.dehancer.com/shop/davinci_resolve/pro
- https://www.dehancer.com/learn/article/faq-prices-and-tariffs
- https://blog.dehancer.com/system-requirements/davinci-ofx-plugins-for-macos/
- https://cdn-files.dehancer.com/65c3322b9be9a5b998b57ab6_README!DaVinciOFXSETUPmacOS.pdf
- https://theotivity.com/review/dehancer-the-cinematic-film-look-made-easy-an-honest-review/ (Feb 2025 prices)
- https://thebytelab.com/dehancer-pro-davinci-resolve/ (Jun 2026 performance notes)
- https://videovillage.com/filmbox/buy
- https://videovillage.com/filmbox/
- https://videovillage.com/scatter/buy
- https://videovillage.com/scatter/
- https://postperspective.com/review-video-villages-filmbox-pro-film-emulation-ofx-plugin/
- https://www.filmconvert.com/purchase
- https://www.filmconvert.com/nitrate
- https://www.provideocoalition.com/cinematch-from-filmconvert/
- https://www.cined.com/anamorphictool-launched-two-ofx-plugins-for-davinci-resolve-fixing-optical-issues-and-adding-anamorphic-lens-characteristics/
- https://anamorphictool.com/ (403)
- https://xere.my/comparisons/best-davinci-vhs-plugins/
- https://xere.my/store/vhs-nostalgia/
- https://pixeltoolspost.com/products/phosphor
- https://blewtoof.mov
- https://www.akascape.com
- https://github.com/Akascape/Rembg-Fuse
- https://github.com/nmbr73/Shaderfuse
- https://github.com/purzbeats/purzos-ofx (+ GitHub API releases: v0.2.0 macos-arm64)
- https://ntsc.rs/docs/openfx-plugin/
- https://github.com/ntsc-rs/ntsc-rs/releases (v0.9.6 macos-openfx.pkg)
- https://github.com/ntsc-rs/ntsc-rs/discussions/127
- https://docs.gyroflow.xyz/app/video-editor-plugins/davinci-resolve-openfx
- https://github.com/gyroflow/gyroflow-plugins (v2.1.1 macOS dmg)
- https://github.com/gyroflow/gyroflow/blob/master/README.md (DJI Action 4/5 support)
- https://github.com/murtazatunio/lenscorrect-ofx
- https://github.com/Microck/boilify
- https://github.com/alexandremendoncaalvaro/CorridorKey-Runtime
- https://github.com/baldavenger/BaldavengerPlugins
- https://github.com/baldavenger/BaldavengerPlugins/issues/4
- https://github.com/Demystify-Color/DMC-BaldavengerOFX-MacOSarm64
- https://github.com/NatronGitHub/openfx-misc
- https://raw.githubusercontent.com/NatronGitHub/openfx-misc/master/README-hosts.txt
- https://github.com/NatronGitHub/openfx-misc/issues/54
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=89570 (Natron OFX in Resolve)
- https://github.com/NatronGitHub/openfx-gmic
- https://github.com/MrKepzie/openfx-gmic
- https://discuss.pixls.us/t/gmic-for-openfx-and-adobe-plugins/452
- https://forum.blackmagicdesign.com/viewtopic.php?f=32&t=75274 (G'MIC OFX not showing in Resolve 15)
- https://github.com/tuttleofx/TuttleOFX
- https://github.com/Greenysmac/awesome-davinci-resolve
- https://github.com/tmoroney/auto-subs (+ releases v3.10.1 Mac-ARM.pkg)
- https://tom-moroney.com/auto-subs/
- https://github.com/octimot/StoryToolkitAI (+ releases v0.25.1)
- https://github.com/octimot/StoryToolkitAI/blob/main/FEATURES.md
- https://docs.topazlabs.com/topaz-video/plugins
- https://docs.topazlabs.com/video-ai/plug-ins
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=197296 (Topaz OFX in Resolve)
- https://www.videoproc.com/resource/topaz-video-ai-review.htm (Aug 2026 pricing)
- https://colourlab.ai/pricing/
- https://4.colourlab.ai/
- https://colourlab.ai/colourlab-ai-for-davinci-resolve/
- https://kiranaistudio.com/ai-sound-design-fusing-elevenlabs-voice-synthesis-with-davinci-resolve/
- https://elevenlabs.io/video/runway-gen-45
- https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_21_New_Features_Guide.pdf?_v=1776322810000 (April 2026; ToC pages 3–6 read)
- https://www.blackmagicdesign.com/products/davinciresolve/whatsnew
- https://larryjordan.com/articles/ai-powered-features-in-davinci-resolve-20/
- https://www.broadcastnow.co.uk/tech-innovation/blackmagic-adds-ai-search-and-voice-creation-in-davinci-resolve-21/5216037.article
- https://www.vp-land.com/p/davinci-resolve-21-adds-nine-ai-tools-for-voice-focus-and-face-editing-plus-a-photo-page-for-still-i
- https://davinciresolveclub.com/davinci-resolve-system-requirements-2026/ (Resolve 21.1 needs macOS 15 + Apple Silicon)
- https://www.izotope.com/en/products/rx.html
- https://www.izotope.com/en/products/release-notes/rx-standard-release-notes
- https://musictech.com/reviews/plug-ins/izotope-rx-12-review/
- https://mixinggpt.com/blog/izotope-rx-12-review-2026
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=65095 (recommended Fairlight plugins)
- https://www.accentize.com/product/dxrevive/
- https://fxfactory.com/info/dxrevive/
- https://www.kvraudio.com/product/dxrevive-by-accentize
- https://www.waves.com/plugins/clarity-vx
- https://equipboard.com/items/waves-clarity-vx-noise-reduction-plug-in
- https://gitlab.com/WeSuckLess/Reactor
- https://kartaverse.github.io/Reactor-Docs/
- https://xere.my/davinci-plugins/reactor/
- https://fxfactory.com/products/applesilicon/davinciresolve/
- https://www.toolfarm.com/compatibility/blackmagic-plugins/ (403)
- https://akvis.com/en/tutorial/ofx-plugins-mac.php (/Library/OFX/Plugins)
- https://resolvedevdoc.readthedocs.io/en/latest/readme_resolveapi.html
- https://deric.github.io/DaVinciResolve-API-Docs/
- https://wiki.dvresolve.com/developer-docs/scripting-api
- https://github.com/brunocbreis/pysion
- https://github.com/Hank-tha-Cowdog/VapourSynth-for-Resolve
- https://forum.blackmagicdesign.com/viewtopic.php?f=38&t=202933 (Python + Fusion AddTool example)
- https://forum.blackmagicdesign.com/viewtopic.php?f=22&t=100818 (ResolveFX not in Fusion Studio)
- https://revisionfx.com/products/for/resolve
- http://www.neatvideo.com/overview.html

---

## Appendix A — all 101 `ofx.` tool IDs in the Fusion registry of DaVinci Resolve Studio 21.1.0 on this Mac (2026-09-22)

Format: `Fusion tool ID | UI name`. Any of these is a valid first argument to `comp.AddTool(...)`.

```
ofx.com.blackmagicdesign.openfx.ColorGeneratorPlugin | Color Generator
ofx.com.blackmagicdesign.resolvefx.Abstraction | Abstraction
ofx.com.blackmagicdesign.resolvefx.AcesTransform | ACES Transform
ofx.com.blackmagicdesign.resolvefx.AnalogDamage | Analog Damage
ofx.com.blackmagicdesign.resolvefx.ApertureDiffraction | Aperture Diffraction
ofx.com.blackmagicdesign.resolvefx.Beauty | Beauty
ofx.com.blackmagicdesign.resolvefx.BlankingFill | Blanking Fill
ofx.com.blackmagicdesign.resolvefx.BlemishRemoval | AI Blemish Removal
ofx.com.blackmagicdesign.resolvefx.BoxBlur | Box Blur
ofx.com.blackmagicdesign.resolvefx.BurnAway | Burn Away
ofx.com.blackmagicdesign.resolvefx.CameraShake | Camera Shake
ofx.com.blackmagicdesign.resolvefx.ChromaticAberration | Chromatic Aberration Removal
ofx.com.blackmagicdesign.resolvefx.ChromaticAdaptation | Chromatic Adaptation
ofx.com.blackmagicdesign.resolvefx.CineFocus | AI CineFocus
ofx.com.blackmagicdesign.resolvefx.CinematicHaze | AI Cinematic Haze
ofx.com.blackmagicdesign.resolvefx.ColorCompressor | Color Compressor
ofx.com.blackmagicdesign.resolvefx.ColorPalette | Color Palette
ofx.com.blackmagicdesign.resolvefx.ColorSpaceTransform | Color Space Transform (Legacy)
ofx.com.blackmagicdesign.resolvefx.ColorSpaceTransformV2 | Color Space Transform
ofx.com.blackmagicdesign.resolvefx.ColorToneDiffuser | ColorTone Diffuser
ofx.com.blackmagicdesign.resolvefx.ContrastPop | Contrast Pop
ofx.com.blackmagicdesign.resolvefx.DCTL | DCTL
ofx.com.blackmagicdesign.resolvefx.DeadPixelFixer | Dead Pixel Fixer (Legacy)
ofx.com.blackmagicdesign.resolvefx.DeadPixelFixerV2 | Dead Pixel Fixer
ofx.com.blackmagicdesign.resolvefx.Deband | Deband
ofx.com.blackmagicdesign.resolvefx.Deflicker | Deflicker
ofx.com.blackmagicdesign.resolvefx.Dehaze | Dehaze
ofx.com.blackmagicdesign.resolvefx.Dent | Dent
ofx.com.blackmagicdesign.resolvefx.DepthMap | AI Depth Map
ofx.com.blackmagicdesign.resolvefx.DespillPlugin | Despill
ofx.com.blackmagicdesign.resolvefx.DetailRecovery | Detail Recovery
ofx.com.blackmagicdesign.resolvefx.DirectionalBlur | Directional Blur
ofx.com.blackmagicdesign.resolvefx.DropShadow | Drop Shadow
ofx.com.blackmagicdesign.resolvefx.DustBuster | Dust Buster (Legacy)
ofx.com.blackmagicdesign.resolvefx.DustBusterV2 | Dust Buster
ofx.com.blackmagicdesign.resolvefx.EdgeDetect | Edge Detect
ofx.com.blackmagicdesign.resolvefx.Emboss | Emboss
ofx.com.blackmagicdesign.resolvefx.FalseColor | False Color
ofx.com.blackmagicdesign.resolvefx.FilmDamage | Film Damage
ofx.com.blackmagicdesign.resolvefx.FilmGrain | Film Grain
ofx.com.blackmagicdesign.resolvefx.FilmLook | Film Look Creator
ofx.com.blackmagicdesign.resolvefx.FlickerAddition | Flicker Addition
ofx.com.blackmagicdesign.resolvefx.FrameReplacer | Frame Replacer
ofx.com.blackmagicdesign.resolvefx.GamutLimiter | Gamut Limiter
ofx.com.blackmagicdesign.resolvefx.GaussianBlur | Gaussian Blur
ofx.com.blackmagicdesign.resolvefx.Glow | Glow
ofx.com.blackmagicdesign.resolvefx.GMSatComp | Gamut Mapping (Legacy)
ofx.com.blackmagicdesign.resolvefx.GMSatCompV2 | Gamut Mapping
ofx.com.blackmagicdesign.resolvefx.Grid | Grid
ofx.com.blackmagicdesign.resolvefx.HalationPlugin | Halation
ofx.com.blackmagicdesign.resolvefx.InvertColor | Invert Color
ofx.com.blackmagicdesign.resolvefx.JPEGDamage | JPEG Damage
ofx.com.blackmagicdesign.resolvefx.LensBlur | Lens Blur
ofx.com.blackmagicdesign.resolvefx.LensDistortion | Lens Distortion
ofx.com.blackmagicdesign.resolvefx.LensFlare | Lens Flare (Legacy)
ofx.com.blackmagicdesign.resolvefx.LensFlareV2 | Lens Flare
ofx.com.blackmagicdesign.resolvefx.LensReflections | Lens Reflections
ofx.com.blackmagicdesign.resolvefx.Lightray | Light Rays
ofx.com.blackmagicdesign.resolvefx.Mirror | Mirrors
ofx.com.blackmagicdesign.resolvefx.MosaicBlur | Mosaic Blur
ofx.com.blackmagicdesign.resolvefx.MotionBlur | Motion Blur
ofx.com.blackmagicdesign.resolvefx.MotionDeblur | AI Motion Deblur
ofx.com.blackmagicdesign.resolvefx.MotionTrails | Motion Trails
ofx.com.blackmagicdesign.resolvefx.NoiseReduction | Noise Reduction
ofx.com.blackmagicdesign.resolvefx.NvidiaRTXHDR | NVIDIA RTX Video HDR
ofx.com.blackmagicdesign.resolvefx.OFX3DKeyer | 3D Keyer (Legacy)
ofx.com.blackmagicdesign.resolvefx.OFX3DKeyerV2 | 3D Keyer
ofx.com.blackmagicdesign.resolvefx.OFXHSLKeyer | HSL Keyer
ofx.com.blackmagicdesign.resolvefx.OFXLumaKeyer | Luma Keyer
ofx.com.blackmagicdesign.resolvefx.PanoMap | PanoMap
ofx.com.blackmagicdesign.resolvefx.PatchReplacer | Patch Replacer
ofx.com.blackmagicdesign.resolvefx.PictureInPicture | Picture In Picture
ofx.com.blackmagicdesign.resolvefx.PrismBlur | Prism Blur
ofx.com.blackmagicdesign.resolvefx.RadialBlur | Radial Blur
ofx.com.blackmagicdesign.resolvefx.Relight | AI Relight
ofx.com.blackmagicdesign.resolvefx.Ripple | Ripples
ofx.com.blackmagicdesign.resolvefx.Scanline | Scanlines (Legacy)
ofx.com.blackmagicdesign.resolvefx.ScanlineV2 | Scanlines
ofx.com.blackmagicdesign.resolvefx.Sharpen | Sharpen
ofx.com.blackmagicdesign.resolvefx.SharpenEdgePlugin | Sharpen Edges
ofx.com.blackmagicdesign.resolvefx.ShrinkAndGrow | Alpha Matte Shrink and Grow
ofx.com.blackmagicdesign.resolvefx.Sketch | Pencil Sketch
ofx.com.blackmagicdesign.resolvefx.Smear | Smear
ofx.com.blackmagicdesign.resolvefx.SoftSharpenSkin | Soften and Sharpen
ofx.com.blackmagicdesign.resolvefx.SplitTone | Split Tone
ofx.com.blackmagicdesign.resolvefx.StopMotion | Stop Motion
ofx.com.blackmagicdesign.resolvefx.Stylize | AI Stylize
ofx.com.blackmagicdesign.resolvefx.SurfaceTracker | Surface Tracker
ofx.com.blackmagicdesign.resolvefx.TexturePop | Texture Pop
ofx.com.blackmagicdesign.resolvefx.TiltShiftBlur | Tilt-Shift Blur
ofx.com.blackmagicdesign.resolvefx.TimelapseDeflicker | Timelapse Deflicker (Legacy)
ofx.com.blackmagicdesign.resolvefx.Transform | Transform
ofx.com.blackmagicdesign.resolvefx.UltraSharpen | AI UltraSharpen
ofx.com.blackmagicdesign.resolvefx.VideoCollage | Video Collage
ofx.com.blackmagicdesign.resolvefx.VideoRestoration | Automatic Dirt Removal
ofx.com.blackmagicdesign.resolvefx.Vignette | Vignette
ofx.com.blackmagicdesign.resolvefx.Vortex | Vortex
ofx.com.blackmagicdesign.resolvefx.Warper | Warper
ofx.com.blackmagicdesign.resolvefx.Watercolor | Watercolor
ofx.com.blackmagicdesign.resolvefx.Waviness | Waviness
ofx.com.blackmagicdesign.resolvefx.ZoomBlur | Zoom Blur
```
