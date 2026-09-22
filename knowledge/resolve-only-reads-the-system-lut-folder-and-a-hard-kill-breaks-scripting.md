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

Timing, same 4x Speed Warp job at 1080p: MacBook 482 s, mini **845 s**. The mini is about 1.8x
slower, so offloading buys a free MacBook, not a faster render.

Related: [[the-mac-mini-has-resolve-studio-and-renders-over-ssh]].
