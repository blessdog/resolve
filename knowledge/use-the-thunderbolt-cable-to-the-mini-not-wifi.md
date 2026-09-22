---
id: use-the-thunderbolt-cable-to-the-mini-not-wifi
kind: verdict
conflict-key: how-to-move-4k-footage-to-the-mac-mini
status: live
verified-on: 2026-09-22
supersedes: [the-mini-must-pull-footage-the-macbook-cannot-push-it]
scope: MacBook Pro and Mac mini joined by a Thunderbolt cable, bridge0 192.168.2.2 <-> 192.168.2.1, macOS 26; measured with nc and with ssh pulling a real 855 MB file
evidence: 855 MB over ssh to 192.168.2.1 in 3.7 s (229 MB/s); raw nc push 8492 MB in 12 s (707 MB/s); the same MacBook on Wi-Fi 15.6 MB/s pulling and 3.7 MB/s pushing
asked-as:
  - copying footage to the mac mini is slow
  - how do I get 4K clips onto the mini for rendering
  - which address should I ssh to the mini on
---

**Talk to the mini on 192.168.2.1, the Thunderbolt bridge. Nothing else comes close, and
nothing reaches it by default.**

| path | throughput | 26 GB takes |
|---|---|---|
| Thunderbolt, raw push | **707 MB/s** | 37 s |
| Thunderbolt, over ssh | **229 MB/s** | 1.9 min |
| Wi-Fi, mini pulling | 15.6 MB/s | 28 min |
| Wi-Fi, MacBook pushing | 3.7 MB/s | 2 h |

**Every obvious address avoids the cable**, which is why this went unnoticed for two days:

- `ryans-mac-mini.local` — mDNS answers with a link-local address on a **100baseTX** adapter
- `192.168.0.31` — the mini's gigabit ethernet, but the MacBook reaches it over **Wi-Fi**
- `192.168.2.1` — the Thunderbolt bridge. The only one that uses the cable.

Fixed in `~/.ssh/config`: `Host mini` now has `HostName 192.168.2.1`, with `mini-wifi` kept as
the fallback for when the cable is out. Ryan, 2026-09-22, on why this matters: *"The reason I
have a whole entire port dedicated to the Mac Mini was to make it a proxy device we can offload
jobs and work to, that can work as seamlessly as it can with the MacBook Pro."*

**The push-versus-pull asymmetry does not exist here.** On Wi-Fi the initiating side mattered
4x; on the cable push is the FASTER direction. That earlier finding was an artifact of a bad
wireless link and is archived.

**Two ways to measure this wrong, both of which I did first.** `/dev/zero` reads 15.8 MB/s while
real video reads 2 — use incompressible data or a real file. And `/dev/urandom` caps around
88 MB/s because generating it is the bottleneck, so it UNDER-reports a fast link by 8x; the
honest number came from moving a file that already existed on disk.

Related: [[the-mac-mini-has-resolve-studio-and-renders-over-ssh]].
