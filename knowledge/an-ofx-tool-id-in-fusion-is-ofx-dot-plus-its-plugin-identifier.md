---
id: an-ofx-tool-id-in-fusion-is-ofx-dot-plus-its-plugin-identifier
kind: verdict
conflict-key: how-to-find-the-fusion-tool-id-of-an-ofx-plugin
status: live
supersedes: []
verified-on: 2026-09-22
scope: DaVinci Resolve Studio 21.1.0 on this MacBook (Apple Silicon); the 101 ofx. tools in a stock install (100 ResolveFX + ColorGenerator); AddTool tested on Glow and HalationPlugin in a hidden fu:NewComp. Third-party OFX ids were NOT dumped here (none installed in /Library/OFX/Plugins at the time); the rule is read from Resolve's own openfx.plugin and libfusionsystem.dylib, so it should hold for them, but each product's identifier string is still unknown until dumped
evidence: docs/research-raw/plugins-2026-09-22/ofx-ai.md §0 and Appendix A (all 101 ids); the dump script in §6 of the same file
asked-as:
  - what is the Fusion tool id of an OFX plugin
  - how do I AddTool a ResolveFX or third-party OFX by script
  - list every ofx. tool Resolve registers
  - why does comp.AddTool of an OFX name return None
---

**A Fusion tool id for any OpenFX effect is the string `"ofx."` followed by the
plugin's own OFX identifier, and the live list comes from the registry, never from
a guess.** Measured on 21.1.0: `resolve:Fusion():GetRegList(CT_Tool)` returned 101
ids beginning `ofx.`, and `comp:AddTool("ofx.com.blackmagicdesign.resolvefx.Glow")`
produced a working `Glow1`. Resolve's own `openfx.plugin` carries the prefix string
and `libfusionsystem.dylib` tests `id:sub(1,35) == "ofx.com.blackmagicdesign.resolvefx."`.

The dump, from a terminal with Resolve open (Lua, because the return shape from
Python was not tested):

    /Applications/DaVinci\ Resolve/DaVinci\ Resolve.app/Contents/Libraries/Fusion/fuscript -l lua -e '
    resolve = bmd.scriptapp("Resolve"); fu = resolve:Fusion()
    for _, reg in ipairs(fu:GetRegList(CT_Tool)) do
      if reg.ID:sub(1,4) == "ofx." then print(reg.ID, "|", reg.Name) end
    end'

The same list sits in `~/Library/Application Support/Blackmagic Design/DaVinci
Resolve/OFXPluginCacheV2.xml` after a scan. For a third-party plugin: install,
relaunch, dump, copy the exact string. Guessing `com.borisfx…` or an enum index is
what cost the spektrafilm session
([[spektrafilm-installs-without-admin-but-its-menus-are-invisible-to-scripting]]).

The boundary this sits inside: OFX is scriptable ONLY on the Fusion page. The
Color page has no AddNode and no OFX parameter access; `ApplyGradeFromDRX` replays a
saved node tree and nothing more ([[the-fusion-page-is-the-only-scriptable-home-for-effects-and-animation]]).
