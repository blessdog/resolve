---
id: spektrafilm-installs-without-admin-but-its-menus-are-invisible-to-scripting
kind: verdict
conflict-key: how-to-install-and-drive-spektrafilm-ofx-in-resolve
status: live
supersedes: []
verified-on: 2026-09-18
scope: spektrafilm OFX 0.4.7 (free, GPL-3.0) on macOS 27, DaVinci Resolve Studio 21.1, driven from the scripting API through a clip's Fusion comp; Osmo clip DJI_20260918143132_0002_D window 55-75 s
evidence: outputs/osmo/2026-09-18-clip-0002/spektra-looks/ (cyan and orange-mask stills from every guessed combination, gitignored); the working install at ~/Library/OFX/Plugins
asked-as:
  - how do I install spektrafilm without an admin password
  - spektrafilm renders cyan or orange garbage
  - can a script drive spektrafilm in Resolve
  - OFX plugin install needs admin rights
---

**It installs with NO admin password, and then cannot be driven blind by script.
The install is a solved problem; the parameters are not.**

Install, verified working: the vendor `.pkg` writes to `/Library/OFX/Plugins`, which needs
admin. Instead `pkgutil --expand` the pkg, `cpio -idm` the Payload, copy the four
`*.ofx.bundle` directories to `~/Library/OFX/Plugins`, and launch Resolve with
`OFX_PLUGIN_PATH="$HOME/Library/OFX/Plugins"` set, running the binary directly
(`/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve`) because `open -a`
does not pass the environment. All four register: `ofx.org.spektrafilm`,
`ofx.org.spektrafilm.flow`, `ofx.org.spektrafilm.lens`, `ofx.org.spektrafilm.diffuse`.
The installer's postinstall step only builds a Metal shader cache and its own script says
installation continues without it.

**Why scripting it blind failed.** Every menu parameter returns `INPIDT_ComboControl_ID`
empty over the API, so `quickInputColorSpace`, `quickPresetCategory`, `quickPresetSelection`,
`process` and `outputRole` are settable only as bare integers with no visible mapping.
Swept 22 input-colour-space values, 4 output roles, 4 process modes and both polarities:
every combination came out cyan-washed or orange (`process` 1 with invert off produced a
textbook orange negative mask, so the engine is working and being fed or read wrong). The
stock names ARE readable from the binary with `strings` (Vision3 50D/200T/250D/500T on 2383
or 2393, Double-X on 2302, Portra, Ektar, Gold, Ultramax, Provia, plus Fuji-on-Endura
combinations), but the name order does not tell you which enum index a menu holds.

**The route that remains:** set it ONCE in the Fusion or colour page inspector, choosing the
input colour space and the preset by NAME, then read the integers back off the live tool with
`GetInput` and write those into a recipe. Do not guess indices again.

Related: [[the-cinematic-levers-ranked-on-the-osmo-exposure-then-optics-then-tone]],
[[film-look-creator-renders-on-the-mini-through-a-fusion-comp]].
