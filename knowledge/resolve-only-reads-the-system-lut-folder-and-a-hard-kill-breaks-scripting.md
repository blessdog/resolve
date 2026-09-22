---
id: resolve-only-reads-the-system-lut-folder-and-a-hard-kill-breaks-scripting
kind: verdict
conflict-key: why-does-setlut-fail-on-a-lut-that-is-installed
status: live
supersedes: []
verified-on: 2026-09-21
scope: DaVinci Resolve Studio 21.1.0.14 on the Mac mini (macOS 26.4.1) driven over ssh; SetLUT on a colour node with a .cube installed under the user Library rather than /Library
evidence: SetLUT returned False with an empty GetLUT for 'film-look/matched/...' while 'Film Looks/Rec709 Kodak 2383 D65.cube' and 'film-look/melara/...' returned True in the same call; an 845 s render completed ungraded because of it
asked-as:
  - SetLUT returns False but the LUT file exists
  - my render came out ungraded
  - where do LUTs have to be installed for Resolve
  - Resolve scripting stopped answering after I killed it
---

**Resolve reads LUTs ONLY from `/Library/Application Support/Blackmagic Design/DaVinci
Resolve/LUT`. A copy in `$HOME/Library/...` is invisible, `SetLUT` returns False, and the
render proceeds ungraded with no other warning.**

That silence is the expensive part: the mini rendered 35.6 s of Speed Warp footage for
845 seconds and produced a correct but completely ungraded file. **Always read `GetLUT(1)`
back after `SetLUT` and fail the run when it is empty.** The system folder turned out to be
`drwxrwxrwx root:staff`, so it is writable with no admin password after all; the earlier
`sudo -n` attempt failed and sent the install to the user folder for nothing.

Copying there over ssh must not use rsync: the path contains spaces and the remote shell
word-splits it (`server receiver mode requires two argument`), which is the already-refuted
[[an-rsync-remote-path-with-a-space-arrives-as-two-arguments]]. `tar cf - matched | ssh mini
'cd "<path>" && tar xf -'` works.

**A new LUT is only seen after Resolve restarts**, the same rule the DCTL list follows in
[[utility-dctls-film-chain-in-resolve-matches-its-published-math]].

**Do not `pkill` Resolve.** After a hard kill the process comes back up and stays running but
`dvr.scriptapp("Resolve")` returns None forever. `osascript -e 'tell application "DaVinci
Resolve" to quit'`, then `open -a`, answers in about 8 seconds.

Timing depends entirely on the job, and the first figure here was over-generalised:

| job | MacBook | mini | ratio |
|---|---|---|---|
| 4x Speed Warp optical flow, 1080p | 482 s | 845 s | 1.75x slower |
| plain graded 4K render, clip 0002 | 244 s | 262 s | **1.07x slower** |
| plain graded 4K render, clip 0004 | 226 s | 232 s | **1.03x slower** |

So the mini is only badly behind on **optical-flow retiming**, which is where its 8 GB and
weaker GPU tell. For an ordinary LUT-and-encode 4K render it is within 7% of the MacBook, and
offloading is nearly free. Measured 2026-09-21 and 2026-09-22 on the same clips.

**The `pkill` warning below is now contradicted and kept only as caution.** On 2026-09-22 the
mini's Resolve ignored an AppleEvent quit at a 300 s timeout AND ignored SIGTERM for twelve and
a half hours at ~750% CPU. `kill -9` finally took it down and **scripting came back completely
normally on relaunch**. See [[resolve-on-the-mini-wedges-at-700-percent-cpu-and-stops-answering]];
prefer a graceful quit, but a hard kill is not the disaster this claim first described. Run the
mini **headless** (`Resolve -nogui`) and the wedge stops happening: with no GUI session there is
no invisible modal, and `StopRendering` returns clean instead of hanging.

Related: [[the-mac-mini-has-resolve-studio-and-renders-over-ssh]].
