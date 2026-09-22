---
id: the-mini-must-pull-footage-the-macbook-cannot-push-it
kind: verdict
superseded-by: use-the-thunderbolt-cable-to-the-mini-not-wifi
conflict-key: how-to-move-4k-footage-to-the-mac-mini
status: superseded
verified-on: 2026-09-21
supersedes: []
scope: MacBook (Wi-Fi 802.11ax, 5 GHz ch36 80 MHz, -67 dBm, 144 Mbps tx rate) to Mac mini (gigabit ethernet, 192.168.0.31) on the same subnet; measured with nc, raw python sockets and curl over http
evidence: same data direction, disk quiet, back to back — mini initiating 15.6 MB/s on 1 GB of real HEVC, MacBook initiating 3.7 MB/s; 31 GB therefore 34 min rather than 4 h
asked-as:
  - copying footage to the mac mini is painfully slow
  - how do I get 4K clips onto the mini for rendering
  - why is the transfer to the mini so slow
---

**SUPERSEDED 2026-09-22.** The asymmetry below is real but it is a WI-FI artifact, and the whole
question was wrong: neither direction should have been on Wi-Fi. The two machines are joined by a
Thunderbolt cable where push runs at 707 MB/s. See
[[use-the-thunderbolt-cable-to-the-mini-not-wifi]].

**Whoever opens the TCP connection decides the speed. The mini must PULL; a push from the
MacBook runs at a quarter of the rate.**

Measured 2026-09-21, both directions carrying MacBook → mini, disk quiet, minutes apart:

| who initiates | throughput | 31 GB takes |
|---|---|---|
| mini pulls | **15.6 MB/s** | 34 min |
| MacBook pushes | 3.7 MB/s | 2 h 20 |

So staging is a one-line HTTP server on the MacBook and a `curl` on the mini:

```
cd <footage dir> && python3 -m http.server 8899 --bind 192.168.0.58
ssh mini 'cd ~/render/src && curl -C - -O http://192.168.0.58:8899/<clip>.MP4'
```

`curl -C -` resumes, so an interrupted stage costs nothing. `scp`/`rsync` from the MacBook are
the slow direction, and rsync additionally cannot take a remote path containing spaces
([[an-rsync-remote-path-with-a-space-arrives-as-two-arguments]]).

**The mechanism is NOT established.** The Wi-Fi link reports a 144 Mbps transmit rate, which
is 18 MB/s, so the pull figure is the honest one and the push is the anomaly; TCP pacing or
Wi-Fi power-save on the initiating side are guesses, not measurements. What is measured is the
4.2x, and it reproduced on nc, on raw sockets and on http.

**Two measurement traps, both of which I fell into first.** Zeros from `/dev/zero` read 15.8 MB/s
even while real video read 2 MB/s, so a throughput test MUST use incompressible payload or a real
file. And a concurrent `sha256` of 60 GB dropped every transfer to ~1 MB/s, which looked exactly
like a network fault — check the disk is idle before believing a network number.

Related: [[the-mac-mini-has-resolve-studio-and-renders-over-ssh]].
