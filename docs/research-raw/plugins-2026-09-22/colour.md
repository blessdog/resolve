# DaVinci Resolve Studio 21 colour ecosystem for a solo creator on Apple Silicon (research date 2026-09-22)

Method: 37 web searches + ~23 page fetches + GitHub API for repo license/activity/last push. Anything a vendor page did not state is marked UNVERIFIED. Piracy mirrors that surfaced in results (memoja, gfx-hub, intro-hd, matesfx/freevideoeffect) were discarded and are not cited.

## Scriptability preamble (read this before the tables)

Verified against the Resolve Scripting API doc for v21.0.4 (X-Raym mirror, updated 2026-07-24; fetched and read). The "no AddNode / no OFX parameter access" finding is corroborated by the search summary of the nobphotographr automation repo (repo itself not read):

| Route | API surface | Status |
|---|---|---|
| `.cube` LUT on an existing node | `TimelineItem.GetNodeGraph().SetLUT(nodeIndex, lutPath)` / `GetLUT()` | VERIFIED in doc. A fresh clip has node 1, so a LUT can be applied with zero UI. |
| `.dctl` on an existing node | `SetLUT()` with a `.dctl` path | UNVERIFIED (DCTLs live in the LUT folder and load via the LUT browser, so plausible; not tested). |
| Any OFX / ResolveFX / Film Look Creator / Dehancer / Filmbox / Neat Video on the Color page | `Graph.ApplyGradeFromDRX(path, gradeMode)` only | VERIFIED: there is **no AddNode**, no way to add an OFX to a node, and no OFX parameter read/write in the Color-page API. The `.drx` must be saved on a machine where that plugin is installed, or the node comes back empty/red. |
| CDL | `TimelineItem.SetCDL({NodeIndex, Slope, Offset, Power, Saturation})`, `Graph.ApplyArriCdlLut()` | VERIFIED in doc. |
| LUT export of a grade | `TimelineItem.ExportLUT(exportType, path)` | VERIFIED in doc. |
| Fusion comp | `comp.AddTool("ofx.<id>")` on the Fusion page | Separate scripting surface. Whether a given colour plugin registers in Fusion is per-plugin and UNVERIFIED for every commercial product below. JP Zambrano ships Fuses that install into Fusion (verified in his README); Baldavenger has a BaldavengerOFX repo (2021), Fuses UNVERIFIED. |

Practical consequence: the "scriptable" column below means (a) `.cube` = direct via `SetLUT`; (b) DCTL = file drop into `/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT` then UNVERIFIED `SetLUT`, certain via `.drx`; (c) OFX/PowerGrade = `.drx` template only.

---

## 1. Film emulation plugins (OFX and OFX-adjacent)

| Name | Maker | URL | Format | Price / license | Resolve 20/21 + Apple Silicon as stated | Scriptable | Why a solo creator wants it | Caveat |
|---|---|---|---|---|---|---|---|---|
| Dehancer Pro | Dehancer | https://www.dehancer.com/shop/davinci_resolve/pro | OFX | Lifetime Individual $1,099 (2 seats), Studio $1,999 (vendor pricing page). Subscription tiers exist but were not shown on the fetched pages: UNVERIFIED. Lite tier exists (Film Profiles, Grain, Bloom, CMY head, Camera Profiles) price UNVERIFIED. | Vendor page: "DaVinci Resolve 19 or newer", macOS 13+, Metal GPU, "optimized for Apple Silicon". 20/21 not named explicitly. Latest v7.4.1 (release date 2026-06-30 from search summary, not vendor page). | `.drx` only | 60+ film profiles, print films, grain, halation, bloom, film damage, LUT generator, DWG/ACES/Cineon pipelines: the most complete one-plugin film look. | Expensive; GPU-heavy on M-series (thebytelab review); "Download & Try" exists but trial/watermark terms not stated on the fetched page (UNVERIFIED). |
| FilmConvert Nitrate | FilmConvert (Rubber Monkey) | https://www.filmconvert.com/purchase?plugin=Ofx | OFX | $119 Resolve-only (RRP $149); all-hosts bundle $179; perpetual (license type not spelled out on page). | Purchase page: "Resolve 16 and later", macOS 10.15+, "Apple Silicon compatible". Latest seen v3.64 (Feb 2025, added LogC4). 20/21 not named. | `.drx` only | 19 stocks scientifically matched to your specific camera profile (camera packs), grain, halation, diffusion; cheapest serious emulator. | Camera-pack dependency: if your camera is not profiled you fall back to generic Rec709 input. |
| Filmbox Pro / Filmbox Looks | Video Village | https://videovillage.com/filmbox/buy | OFX | Looks: $29/qtr, $69/yr, $199 perpetual (1 activation). Pro: $129/qtr, $349/yr, $999 perpetual (2 activations). Sub payments credit up to 50% toward perpetual. 14-day trial, no watermark, card required. | macOS 12+; Resolve/Baselight/Premiere/AE/FCP hosts. Apple Silicon and Resolve version not explicitly stated on buy page. | `.drx` only | Considered the reference-grade Kodak negative+print emulation; Looks tier is the cheapest "it just looks like film" button. | Licensed only for productions under $5M budget; Looks tier hides most controls. |
| Scatter | Video Village | https://videovillage.com/scatter/ | OFX (format not stated on page; sibling of Filmbox) | Price not shown on product page: UNVERIFIED | Same host list as Filmbox; system requirements not shown | `.drx` only | Physically-modelled optical diffusion (Black Pro-Mist etc.) without the light loss of glass. | Pricing hidden behind Buy; UNVERIFIED. |
| Magic Bullet Looks (Magic Bullet Suite 2026) | Maxon / Red Giant | https://www.maxon.net/en/red-giant | OFX | Subscription only: Red Giant Complete $79/mo or $599/yr; Maxon One $149/mo or $1,199/yr. No perpetual. | Maxon's own requirements page returned 403. The only Maxon page reachable is the stale Suite 14 (2021) article saying NO Apple Silicon and Resolve 14-17. Third-party (phoenix3dart, 2026-02) says current suite is Apple Silicon native. Resolve 20/21 support UNVERIFIED. | `.drx` only | Preset-browser look design with 100s of looks, film stocks, halation, diffusion; fast for non-colorists. | Subscription-only, priced for the whole suite; Resolve 21 compatibility not confirmed by Maxon. |
| Colourlab Ai 3 (Look Designer + Grainlab plugins) | Color Intelligence | https://colourlab.ai/pricing/ | Standalone app + OFX plugins for Resolve | Creator $15/mo or $150/yr; Pro $39/mo or $400/yr; Studio $49/mo or $500/yr; perpetual $299 (Creator features). The Resolve Look Designer and Grainlab **plugins sit only in the Studio tier**. (A search summary claimed $995 Pro perpetual; the fetched pricing page does not show it, so use the page.) | "Mac OS 13+ and Windows 10+"; Apple Silicon and Resolve version not stated. | `.drx` for plugins; the standalone app round-trips via Resolve timeline sync, not the Python API | AI shot-matching and one-click balance across a whole timeline: the fastest "make 200 clips consistent" tool. | The bits that live inside Resolve need the $49/mo tier; perpetual buys only Creator features. |
| ARRI Film Lab | ARRI, sold by RE:Vision Effects | https://revisionfx.com/products/arrifilmlab/ | OFX | $25/mo, $250/yr, $500 permanent (individual); floating +~20%. | Hosts: Resolve & Fusion Studio, Baselight, Nuke, Flame etc. macOS/Windows/Linux. Apple Silicon and Resolve 20/21 not stated: UNVERIFIED. Released Nov 2025. | `.drx` only | ARRI's own scanned-stock grain, halation, gate weave; real-time 4K. | New (2025-11); LogC3/LogC4-centric pipeline, so non-ARRI cameras need a CST first. |
| EMUL8 | Cinem8 (Christian Maté Grab, Eric Lenz) | https://cinem8.co/products/emul8-film-emulation-for-davinci-resolve | DCTL + PowerGrade (not OFX) | EUR 149 one-time, lifetime updates | Vendor page: "DaVinci Resolve Studio only – version 19.1.1 or newer", macOS 11+, "Apple SoC Pro-line recommended", 16 GB RAM | DCTL file drop + `.drx` | 17 Kodak/Fuji-modelled looks plus halation, bloom, 8mm-65mm grain; drag-and-drop install. | Grain via DCTL is GPU-heavy on base M-chips (vendor recommends Pro line). |
| Film/Emulsion | PixelTools | https://pixeltoolspost.com/products/film-emulsion | OFX (Pro) or DCTL set | Perpetual, one-time (exact price not fetched: UNVERIFIED); PixelTools all-DCTL bundle $819.99 | Not stated on fetched pages: UNVERIFIED | DCTL drop / `.drx` | Node-based negative, print, halation, grain you can pull apart and learn from. | Sits in an expensive catalogue; buy the single product, not the bundle. |
| FilmX Emulation | The Resolve Store | https://theresolve.store/filmx-emulation-for-davinci-resolve/ | DCTL | Paid; price UNVERIFIED | UNVERIFIED | DCTL drop | 21-28 stocks coded natively in DCTL, lighter than OFX. | Vendor claims only; no independent review found. |
| CinePrint35 | Tom Bolles | https://www.tombolles.net/cineprint35 | PowerGrade (.drx) + LUTs, native nodes only | Paid; price UNVERIFIED | Native nodes, so anything Resolve 17+ runs it | `.drx` direct via `ApplyGradeFromDRX` | 16mm/35mm looks built from native nodes: fully editable and the most scriptable emulation on this list. | Not a plugin; no camera matching. |
| spektrafilm OFX | spektrafilm.114c.de | https://spektrafilm.114c.de | OFX | Free beta | UNVERIFIED | `.drx` only | Spectral negative/print/scan model for free. | Beta; found only via awesome-list, not independently verified. |
| "Emery" | NOT FOUND | — | — | — | — | — | Searched "Emery film emulation DaVinci Resolve", "Emery DCTL OR OFX OR PowerGrade", "Emery LUTs / Emery Film / Emery Looks". No product of that name surfaced. Possibly a misremembering of EMUL8 or Film/Emulsion. | NOT FOUND |

## 2. Free DCTL libraries (GitHub API checked 2026-09-22: last push, license, stars)

| Name | Maker | URL | Format | License | Maintained? (last push) | Scriptable | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| OpenDRT (open-display-transform) | Jed Smith | https://github.com/jedypod/open-display-transform | DCTL (+ Nuke) | GPL-3.0 | Yes: pushed 2026-02-09; latest release v1.1.0 (2025-01-22) with DCI presets, look presets, "Stickshift" all-params variant | DCTL drop; 519 stars | Best free scene-referred display transform: replaces the ACES/DaVinci tone mapper with something that holds highlights and skin. | GPL: fine for use, matters only if you redistribute. Needs a scene-linear/log input pipeline (CST first). |
| Baldavenger DCTLs | Paul Dore | https://github.com/baldavenger/DCTLs | DCTL (+ OFX + Fuses in sibling repos) | GPL-3.0 | Stale: DCTLs pushed 2023-12-06; ACES_DCTL 2021-08-30; BaldavengerOFX 2021-10 | DCTL drop; Fuses install to Fusion | Huge grab-bag: ACES tools, film grain, hue-vs-hue, false colour, zone system. | Last push 2023-12; no statement of Resolve 20/21 compatibility anywhere in the repo pages fetched. |
| JuanPabloZambrano/DCTL (2499 DRT, Jp-DRT, AgxDRT, GuardRail) | Juan Pablo Zambrano | https://github.com/JuanPabloZambrano/DCTL | DCTL + Fuses | NO LICENSE FILE (all rights reserved by default) | Yes: pushed 2025-11-06; 322 stars | DCTL drop; Fuses to Fusion | 2499 DRT is a beloved filmic display transform; GuardRail gamut clamp. | No license = legally grey to redistribute or embed. jedypod/JP2499 exists as "fork from before it went closed source", so the open status has been contested. |
| AgX-Resolve | Troy Sobotka + Jed Smith + JP Zambrano | https://github.com/sobotka/AgX-Resolve | DCTL | NO LICENSE FILE | Pushed 2024-11-25 | DCTL drop | Blender's AgX picture formation for Resolve; very forgiving on saturated LEDs. | No license file; not updated in ~22 months. |
| Nick Shaw gamut_mapping | Nick Shaw (Antler Post) | https://github.com/nick-shaw/gamut_mapping | DCTL | NO LICENSE FILE | Stale: 2020-05-18 | DCTL drop | Reference implementation of the ACES gamut compressor as a DCTL. | Superseded by Resolve's built-in Gamut Mapping and ACES 1.3 RGC; historical interest. |
| Demystify-Color DCTLs | Nico Fink | https://github.com/Demystify-Color/DCTLs | DCTL | MIT | Yes: pushed 2026-05-22; 161 stars | DCTL drop | Free, MIT, tutorial-backed (demystify-color.com/dctl-coding): the best place to learn DCTL. | Paid "Beyond Film Emulation" pack is separate. |
| Tetra-DCTLOFX | npeason | https://github.com/npeason/Tetra-DCTLOFX | DCTL | MIT | Stale: 2021-03-13; 197 stars | DCTL drop | Steve Yedlin-style tetrahedral RGB matrix ("Tetra") tool, free. | Unmaintained; still compiles (simple code). |
| Tetrahedral-Interpolation-for-Fusion | EmberLightVFX | https://github.com/EmberLightVFX/Tetrahedral-Interpolation-for-Fusion | Fuse (DCTL-based) + macro | MIT | Stale: 2021-04-19 | Fusion `AddTool` | Same Tetra idea for the Fusion page. | Unmaintained. |
| xtremestuff/resolve-dctl | xtremestuff | https://github.com/xtremestuff/resolve-dctl | DCTL library | MIT | Yes: pushed 2026-04-10; 163 stars | DCTL drop | Actively maintained utility library; sibling protune-transforms repo covers GoPro GP-Log. | UNVERIFIED contents beyond README. |
| MoazElgabry/DCTLs | Moaz Elgabry | https://github.com/MoazElgabry/DCTLs | DCTL | GPL-3.0 | Yes: pushed 2026-06-13 | DCTL drop | Look-dev and grading tools, actively updated. | Smaller community (68 stars). |
| mitkunz/resolve_DCTLs | mitkunz | https://github.com/mitkunz/resolve_DCTLs | DCTL | GPL-3.0 | Pushed 2025-07-20 | DCTL drop | Technicolor-style RGB mixing, film saturation. | Small. |
| mikaelsundell/photographic-dctls | Mikael Sundell | https://github.com/mikaelsundell/photographic-dctls | DCTL | NO LICENSE FILE | Yes: pushed 2026-06-05 | DCTL drop | LogC, ACES AP0, Cineon math experiments. | No license file. |
| ra100/dctl-utils | ra100 | https://github.com/ra100/dctl-utils | DCTL | GPL-3.0 | Stale: 2023-12-20 | DCTL drop | Skin-tone indicator with tolerances. | Small, stale. |
| thatcherfreeman/utility-dctls | Thatcher Freeman | https://github.com/thatcherfreeman/utility-dctls | DCTL | MIT | Yes: pushed 2026-09-22 (today); 423 stars | DCTL drop | (Already known to caller; listed for completeness of the maintenance check.) | — |
| MONONODES DCTLs | Mononodes | https://mononodes.com/dctls/ | DCTL (paid) | Commercial | Active store | DCTL drop | NOT FREE: the task filed this under free libraries; it is a paid store (Utility DCTLs, Film Elements, Color Shift, Grid). | Prices not fetched: UNVERIFIED. |
| PixelTools | PixelTools | https://pixeltoolspost.com/pages/free-toolkit-for-davinci-resolve | DCTL + OFX + PowerGrade (paid, one free kit) | Commercial, perpetual, lifetime updates; all-DCTL bundle $819.99; free newsletter kit = 2 DCTLs + 1 PowerGrade | Active | DCTL drop / `.drx` | NOT FREE except the newsletter kit; Prime/Grade is OFX+DCTL. | Expensive catalogue. |

## 3. PowerGrades and LUT packs (free and paid)

| Name | Maker | URL | Format | Price | Resolve compat | Scriptable | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| Darren Mostyn | Darren Mostyn (BMD Master Trainer) | https://www.motionvfx.com/darren-mostyn | Curated MotionVFX .drfx recommendations | — | — | — | No first-party Mostyn PowerGrade pack located; the MotionVFX page is a recommendation page (fetch returned header only). Nearest thing: Ryan Velting's Basic/Pro/Advanced PowerGrades "based on techniques by Darren Mostyn, Cullen Kelly and Danny Gan" at https://ryanvelting.com/shop/p/pro-davinci-resolve-powergrade (price UNVERIFIED). | NOT FOUND as a product. |
| Dawson Colour | — | — | — | — | — | — | Searched "Dawson Colour DaVinci Resolve PowerGrade", "Dawson colour grading PowerGrade LUT pack", "Dawson DaVinci Resolve colorist YouTube free PowerGrade DCTL". Nothing surfaced. | NOT FOUND. |
| Qazi's Toolkit | Waqas Qazi | https://www.qazistoolkit.com/ | 8 DCTLs (Look DNA, Skin Juice Mixer, Color Compressor, Charts, Saturation Control, Skin Compressor, Halation, Film Density) | $776 one-time (list $1,473); VIP $1,497; lifetime updates; no refunds | Vendor: Studio only; "Apple M1/M2" minimum CPU, 16 GB RAM, 4 GB VRAM | DCTL drop | Skin-focused DCTLs from a working commercial colorist. | Very expensive for what are DCTL files; marketing-heavy. |
| RapidGrade | Waqas Qazi | https://www.getrapidgrade.com/ | "plugin engine" (format not disclosed; OFX per courses.waqasqazi.com/rapidgrade-ofx) | Lifetime $699 (2 seats), Annual $299, Monthly $149; 7-day refund | Not stated: UNVERIFIED | `.drx` only if OFX | One-click looks + 52 new looks/yr. | Price is in Filmbox Pro territory. |
| "Qazi's Colorist Factory" | — | https://coloristfactory.com | — | — | — | — | coloristfactory.com no longer resolves in DNS (2026-09-22, two attempts). It appears to have been a separate tutorial/LUT site (author UNVERIFIED); no connection to Qazi found in any result. The only trace is a 2022 tetrahedral-interpolation blog post title in search results (never read). | Domain dead; treat as defunct. |
| Tom Antos | Tom Antos | (no first-party page found) | — | — | — | — | Searches for a Tom Antos Kodak 2383 pack found nothing first-party. | NOT FOUND. |
| Casey Faris / Ground Control | Ground Control | https://groundcontrol.film/ | Courses; PowerGrades bundled in courses | Course-priced ($249 class) | — | — | Training, not a grade pack. No standalone PowerGrade found. | NOT a product. |
| Kodak 2383: Cine Source LogC 2383 | Cine Source | https://cinesource.nl/products/logc-kodak-2383-lut/ | .cube | Free | Any | `SetLUT` direct | Built as a "better alternative to Resolve's built-in 2383"; LogC input. | LogC-input: CST to LogC3 first. |
| Kodak 2383: ProColor free LUT | procolor.ist | https://procolor.ist/freelut/ | .cube (DWG/ACES scene-referred) | Free | Any | `SetLUT` direct | Scene-referred in DWG or ACES, so it drops into a colour-managed Resolve project as-is. | Sign-up gate UNVERIFIED. |
| Kodak 2383: DD free LUT | djobd (Gumroad) | https://djobd.gumroad.com/l/free_dd_kodak_2383_lut | .cube | Free | Any | `SetLUT` direct | Built inside Resolve; quick. | Input space UNVERIFIED. |
| Kodak 2383 D55 | imnz730 | https://github.com/imnz730/LUTs | .cube | Free (GitHub) | Any | `SetLUT` direct | Rec709 input, one file, no sign-up. | License UNVERIFIED. |
| Kodak 2383 PowerGrade (native) | Grade Atlas curated | https://www.gradeatlas.com/free-powergrades | .drx | Free | Any | `ApplyGradeFromDRX` direct | Curated list of free PowerGrades linking to original creators. | Quality varies. |
| Beyond Film Emulation (scene-ref) | Demystify Color (Nico Fink) | https://www.demystify-color.com/product-page/beyond-film-emulation-dctl-luts-scene-referred | DCTL + LUT + PowerGrade for DWG/LogC3/ACES | Paid, price UNVERIFIED | Studio for DCTL | DCTL / `.drx` / `SetLUT` | From the author of the MIT free DCTLs; scene-referred. | — |
| PowerGrade Bundle | PixelTools | https://pixeltoolspost.com/products/powergrade-bundle | .drx | $299.99 | Any | `ApplyGradeFromDRX` direct | Native-node grades, perpetual. | Pricey. |
| Free basic node tree | Brock Roberts | https://brock-roberts-films.sellfy.store/p/powergrade/ | .drx | Free | Any | `ApplyGradeFromDRX` | A sane starter node tree for scripting against (fixed node indices). | — |
| FILMIC 3.0 kit | veresdenialex | https://www.veresdenialex.com/product-page/sony-classic-film-s-log-to-rec709 | .cube + .drx | Free | Any | both | Sony S-Log to Rec709 filmic. | Sony-specific. |
| The Vault 30+ PowerGrades | Melior Studios | https://meliorstudios.com/store/p/the-45-powergrades | .drx + LUTs | Paid, price UNVERIFIED | Any | `ApplyGradeFromDRX` | Volume pack. | Quality UNVERIFIED. |

## 4. Camera-specific: DJI Osmo Action 5 Pro D-Log M and iPhone Apple Log / Apple Log 2

| Name | Maker | URL | Format | Price | Compat | Scriptable | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| OA5P D-Log M to Rec.709 Vivid LUT (official) | DJI | https://www.dji.com/downloads/softwares/dji-osmo-action-5-pro-d-log-m-to-rec-709-vivid-lut | .cube | Free | Any | `SetLUT` direct | The only vendor-authored transform for OA5P D-Log M. | It is a "vivid" look, not a neutral technical transform. BMD forum thread reports Resolve's built-in D-Log CST preset is the wrong curve for D-Log M (forum-sourced). |
| Palermo PowerGrade & LUTs (D-Log M) | Ed Prosser | https://edprosser-shop.fourthwall.com/en-gbp/products/palermo-powergrade | .drx + 15 .cube | Paid, price UNVERIFIED | Vendor: Resolve Studio 18+ | `.drx` direct + `SetLUT` | Built specifically for OA5P D-Log M; base LUT + stackable looks. | Studio required. |
| DJI Osmo Action Film LUTs | Cinem8 | https://cinem8.co/products/cinematic-film-luts-dji-osmo-action-5 | .cube (D-Log M to Rec709 conversion + finishing LUTs) | Paid, price UNVERIFIED | Any .cube host | `SetLUT` direct | Two-stage: technical conversion then film look. | Must apply conversion LUT first. |
| ROMA PowerGrade + Action 4/5 D-Log M LUT | Roma Fedorov | https://romafedorov.gumroad.com | .cube + .drx | Paid, UNVERIFIED | — | both | Action-cam-specific. | Little documentation. |
| Color Grade for Osmo Action 4/5/6 | Ski Across Japan | https://www.skiacrossjapan.com/store-FV4A4/p/color-grade-for-dji-osmo-action-456-in-davinci-resolve | PowerGrade | Paid, UNVERIFIED | — | `.drx` | Outdoor/snow-tuned. | Niche. |
| Apple Log 2 to Rec.709 conversion LUT | Rodrigo Polo | https://rodrigopolo.com/2025/11/04/apple-log-2-to-rec-709-conversion-lut/ | .cube 33-pt (monitors) and 65-pt (Resolve/Premiere), four files | Free (tip jar) | Any | `SetLUT` direct | The cleanest free technical Log 2 to Rec709 for iPhone 17 Pro; also covers ProRes RAW via Atomos. | Not scene-referred; author's blog also has an iPhone HDR-in-Resolve guide worth reading. |
| Apple LOG "Filmic Looks" | Tobia Montanari | https://www.tobiamontanari.com/apple-log-filmic-looks-luts/ | .cube (3x Kodak 2383, 3x Fuji 3513DI, white-point variants) | Kodak D65 LUT free; full pack now paid (30% code FILMIC30) | Any; supports Apple Log and Apple Log 2 (iPhone 17 Pro+) | `SetLUT` direct | One LUT does Log-to-709 plus print look. | Was free, now mostly paid. |
| Apple Log / Log 2 conversion LUTs | LUT Co | https://lutcompany.com/store/apple-log-to-rec709-creative-iphone-15-pro-luts | .cube (Log to 709, Log 2 to 709 std/bold, Log 2 to DWG, Log 2 to Arri709) | Paid, UNVERIFIED | Any | `SetLUT` direct | The Log 2 to DWG variant is the right thing for a colour-managed project. | Price UNVERIFIED. |
| Free Apple conversion LUTs (iPhone 17 Pro) | gamut.io | https://gamut.io/product/free-apple-conversion-luts-iphone/ | .cube | Free | — | `SetLUT` | Listed as free Log 2 conversions. | Page returned 403; contents UNVERIFIED. |
| Native: Resolve CST "Apple Log" | Blackmagic | built-in | CST node | Included | UNVERIFIED in this research | `.drx` | If Apple Log (v1) and Apple Log 2 are present in the Color Space Transform input list, no LUT is needed at all. NEITHER was verified here: check the CST dropdown in Resolve 21 before routing iPhone footage on it. | Forum claim that Apple's own v1 LUT ruins iPhone 16 Pro skin tones is a forum claim, not verified. |

## 5. Native Resolve 20 / 21 colour features worth knowing (all built-in)

| Feature | Version | Studio-only? | Scriptable | Why | Caveat |
|---|---|---|---|---|---|
| Film Look Creator | 19.0; 20.1 added natural + strong split-tone modes | Yes (BMD: Studio-only, scene-referred) | `.drx` only | Free-with-Studio film emulation: presets (Rochester, Akasaka, Elated, Vintage), grain, halation, bloom, gate weave. Replaces a $199-999 plugin for many creators. | No changes located for 21; best in DWG/Intermediate. |
| Color Slice | 19.0 | UNVERIFIED (Color page tool, likely both) | `.drx` | Seven vectors (RYGCBM + skin) with density and subtractive saturation: skin fixes without qualifiers. | Correction to task premise: introduced in 19, not 18.6. |
| Chroma Warp | 20.0 | UNVERIFIED | `.drx` | Drag hue+sat in the viewer in one motion. | — |
| Magic Mask v2, Depth Map v2 | 20.0 | Yes | `.drx` | Better isolation for targeted grades. | GPU/Neural Engine heavy. |
| AI Cinematic Haze | 20.2 | Yes | `.drx` | Depth-aware atmosphere. | — |
| Glow / Light Rays atmosphere controls | 20.1 | Yes | `.drx` | Secondary glow, RGB rays. | — |
| Layer List view in Node Editor | 21.0 | UNVERIFIED | — | Nodes as rows; easier to reason about fixed node indices for `SetLUT(nodeIndex)`. | UI only. |
| Group Colour Grade Versions | 21.0 | UNVERIFIED | Version API (`AddVersion`, `LoadVersionByName`) | Multiple grade versions per group. | — |
| MultiMaster trim passes (individual trims in 21.1) | 21.0 / 21.1 | Yes | UNVERIFIED | HDR + SDR deliverables from one timeline. | Overkill for solo SDR. |
| Magic Mask Render in Place | 21.0 | Yes | — | Cache tracked masks as travelling-matte nodes. | — |
| AI CineFocus, Face Age Transformer, Face Reshaper, Blemish Removal, UltraSharpen, Motion Deblur | 21.0 | Yes (AI tools are Studio) | `.drx` | CineFocus = keyframable fake DoF; UltraSharpen for soft action-cam footage. | Per-feature Studio status UNVERIFIED on BMD page. |
| Photo page | 21.0 | UNVERIFIED | UNVERIFIED | Node grading for stills, shared nodes across an album. | New surface; API coverage unknown. |

## 6. Denoise / cleanup

| Name | Maker | URL | Format | Price | Compat | Scriptable | Why | Caveat |
|---|---|---|---|---|---|---|---|---|
| Neat Video 6 for DaVinci Resolve | ABSoft | https://www.neatvideo.com/download | OFX (dedicated Resolve build) | Home $89.90 (1080p, 1 GPU, non-commercial); Pro $159.90 (unlimited, commercial). Reported via Toolfarm/reviews. | Reported: 6.1.3 (May 2026) adds Resolve 21; Apple Silicon incl. M4 supported; macOS 11+. neatvideo.com returned HTTP 418 twice, so vendor page NOT verified. | `.drx` only (and noise profile must be built per clip) | Still the reference denoiser; GPU-shared frame exchange with Resolve. | PURCHASE GOTCHA: the generic "Neat Video for OFX" edition (Pro $249.90 / Studio $349.90) does NOT support Resolve; buy the dedicated "for DaVinci Resolve" edition ($89.90/$159.90). Slow on long timelines; profile per shot. |
| Resolve native Temporal/Spatial NR | Blackmagic | built-in (Motion Effects palette) | built-in | Included with Studio | Studio-only | `.drx` | Good enough for mild ISO noise; zero cost. | Softens fine texture at high strengths; no profiling. |
| Topaz Video (AI) | Topaz Labs | https://www.topazlabs.com | Standalone; Resolve plugin claimed | Subscription only since Oct 2025 | Apple Silicon native standalone | none (external round-trip) | Heavy-noise rescue and upscaling. | Perpetual ended Oct 2025; Resolve plugin UNVERIFIED. |
| Boris FX Continuum (BCC Denoise) | Boris FX | https://borisfx.com | OFX | Subscription | — | `.drx` | Broad suite. | No 2025-26 Resolve-specific denoise evidence surfaced: UNVERIFIED. |
| RE:Vision DE:Noise | RE:Vision Effects | http://revisionfx.com/products/for/resolve | OFX | Paid, UNVERIFIED | Resolve host listed | `.drx` | Alternative OFX denoiser from a long-standing Resolve vendor. | UNVERIFIED pricing. |
| AI UltraSharpen / Motion Deblur | Blackmagic | built-in (21) | ResolveFX | Studio | 21 | `.drx` | Post-denoise sharpening. | — |

## Top picks for a solo creator (Apple Silicon, Resolve Studio 21)

Free-first stack, all scriptable today: keep footage in DaVinci YRGB Color Managed, convert iPhone Log 2 with Rodrigo Polo's free 65-pt LUT (or the native CST if Log 2 appears in 21), use DJI's official D-Log M LUT for the OA5P, drop OpenDRT v1.1.0 (GPL, maintained) or AgX as the display transform, use Color Slice for skin, Film Look Creator for grain/halation, native temporal NR for noise, and a free Kodak 2383 .cube (ProColor scene-referred or Cine Source) as the print look. Every piece is a `.cube`/`.dctl` file or a `.drx` template, which is exactly what `Graph.SetLUT` and `ApplyGradeFromDRX` can drive from Python. First paid tier, in order of value: FilmConvert Nitrate $119 perpetual (cheapest real film emulation), Filmbox Looks $199 perpetual (best-looking one-button film), Neat Video Pro $159.90 (when native NR is not enough), Demystify Color's MIT DCTLs plus his paid scene-referred pack if you want to learn the maths. Skip for now: Dehancer at $1,099, Qazi Toolkit at $776, RapidGrade at $699, and anything subscription-only (Magic Bullet, Topaz, Colourlab Studio tier) until a job pays for it.

## Not found / could not verify (state plainly)

- "Emery" film emulation: NOT FOUND under any phrasing.
- "Dawson Colour": NOT FOUND.
- "Qazi's Colorist Factory": coloristfactory.com does not resolve in DNS; it was not a Qazi property.
- Darren Mostyn: no first-party PowerGrade product; MotionVFX page is a recommendation page.
- Tom Antos 2383 pack: no first-party page located.
- Fetch failures: neatvideo.com (418 twice), gamut.io (403), Maxon support (403), coloristfactory.com (DNS, twice), motionvfx.com/darren-mostyn (returned header only).
- Seen only as search-result titles, never read: mhadifilms v20.3 API gist, nobphotographr automation repo, coloristfactory 2022 blog post.

## Sources

- https://www.dehancer.com/shop/davinci_resolve/pro
- https://www.dehancer.com/pricing/lifetime/davinci_resolve
- https://www.dehancer.com/shop/video/davinci_resolve
- https://thebytelab.com/dehancer-pro-davinci-resolve/
- https://www.filmconvert.com/purchase?plugin=Ofx
- https://www.filmconvert.com/download/software-updates?Product=nitrate
- https://videovillage.com/filmbox/buy
- https://videovillage.com/filmbox/
- https://videovillage.com/scatter/
- https://xere.my/davinci-plugins/filmbox/
- https://colourlab.ai/pricing/
- https://www.cgchannel.com/2024/10/color-intelligence-releases-colourlab-ai-3/
- https://www.maxon.net/en/red-giant
- https://support.maxon.net/hc/en-us/articles/4411955771922-Magic-Bullet-Suite-14-Compatibility-System-Requirements
- https://www.phoenix3dart.com/2026/02/red-giant-magic-bullet-suite.html
- https://revisionfx.com/products/arrifilmlab/
- https://www.cined.com/arri-film-lab-announced-real-time-analog-film-emulation-plugin-for-davinci-resolve-baselight-nuke/
- https://www.newsshooter.com/2025/12/21/arri-film-lab-review/
- https://cinem8.co/products/emul8-film-emulation-for-davinci-resolve
- https://pixeltoolspost.com/products/film-emulsion
- https://pixeltoolspost.com/products/pixeltools-dctl-plug-in-bundle
- https://pixeltoolspost.com/pages/free-toolkit-for-davinci-resolve
- https://pixeltoolspost.com/products/powergrade-bundle
- https://theresolve.store/filmx-emulation-for-davinci-resolve/
- https://www.tombolles.net/cineprint35
- https://github.com/Greenysmac/awesome-davinci-resolve
- https://github.com/jedypod/open-display-transform/releases
- https://github.com/baldavenger/DCTLs
- https://github.com/baldavenger/ACES_DCTL
- https://github.com/JuanPabloZambrano/DCTL
- https://github.com/jedypod/JP2499
- https://github.com/sobotka/AgX-Resolve
- https://github.com/nick-shaw/gamut_mapping
- https://github.com/Demystify-Color/DCTLs
- https://github.com/npeason/Tetra-DCTLOFX
- https://github.com/EmberLightVFX/Tetrahedral-Interpolation-for-Fusion
- https://github.com/xtremestuff/resolve-dctl
- https://github.com/MoazElgabry/DCTLs
- https://github.com/mitkunz/resolve_DCTLs
- https://github.com/mikaelsundell/photographic-dctls
- https://github.com/ra100/dctl-utils
- https://github.com/thatcherfreeman/utility-dctls
- https://mononodes.com/dctls/
- https://www.motionvfx.com/darren-mostyn
- https://ryanvelting.com/shop/p/pro-davinci-resolve-powergrade
- https://www.qazistoolkit.com/
- https://www.getrapidgrade.com/
- https://www.qazverse.com/
- https://groundcontrol.film/
- https://cinesource.nl/products/logc-kodak-2383-lut/
- https://procolor.ist/freelut/
- https://djobd.gumroad.com/l/free_dd_kodak_2383_lut
- https://github.com/imnz730/LUTs
- https://www.gradeatlas.com/free-powergrades
- https://www.demystify-color.com/product-page/beyond-film-emulation-dctl-luts-scene-referred
- https://brock-roberts-films.sellfy.store/p/powergrade/
- https://www.veresdenialex.com/product-page/sony-classic-film-s-log-to-rec709
- https://meliorstudios.com/store/p/the-45-powergrades
- https://www.dji.com/downloads/softwares/dji-osmo-action-5-pro-d-log-m-to-rec-709-vivid-lut
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=192412
- https://edprosser-shop.fourthwall.com/en-gbp/products/palermo-powergrade
- https://cinem8.co/products/cinematic-film-luts-dji-osmo-action-5
- https://romafedorov.gumroad.com
- https://www.skiacrossjapan.com/store-FV4A4/p/color-grade-for-dji-osmo-action-456-in-davinci-resolve
- https://rodrigopolo.com/2025/11/04/apple-log-2-to-rec-709-conversion-lut/
- https://rodrigopolo.com/2025/11/20/iphone-hdr-video-in-resolve-the-right-way/
- https://www.tobiamontanari.com/apple-log-filmic-looks-luts/
- https://lutcompany.com/store/apple-log-to-rec709-creative-iphone-15-pro-luts
- https://gamut.io/product/free-apple-conversion-luts-iphone/
- https://discussions.apple.com/thread/256044678
- https://www.blackmagicdesign.com/products/davinciresolve/whatsnew
- https://www.redsharknews.com/davinci-resolve-21-nab-2026-photo-page-ai-tools
- https://www.redsharknews.com/davinci-resolve-21.1-new-features-release
- https://www.cgchannel.com/2025/08/blackmagic-design-releases-davinci-resolve-20-1/
- https://www.cgchannel.com/2025/09/blackmagic-design-releases-davinci-resolve-20-2/
- https://www.newsshooter.com/2025/04/04/blackmagic-design-davinci-resolve-20-announced-with-100-new-features-including-ai-enhancements/
- https://blog.frame.io/2024/08/15/what-is-resolves-new-film-look-creator-plugin/
- https://digitalfilms.wordpress.com/2024/10/05/davinci-resolve-19-colorslice/
- https://www.videoeditorlondon.co.uk/post/how-to-use-colorslice-in-davinci-resolve
- https://www.neatvideo.com/news/neat-video-6
- https://www.toolfarm.com/buy/neat_video_pro_for_davinci_resolve/
- https://mixinglight.com/color-grading-tutorials/noise-reduction-in-resolve-part-2-neat-video-ofx-plug-in/
- https://unifab.ai/resource/neat-video
- https://www.aiarty.com/ai-video-enhancer/topaz-video-vs-davinci-resolve.htm
- http://revisionfx.com/products/for/resolve
- https://gist.github.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8
- https://github.com/nobphotographr/davinci-resolve-automation
