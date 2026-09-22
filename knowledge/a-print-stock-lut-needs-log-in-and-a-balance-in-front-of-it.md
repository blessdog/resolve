---
id: a-print-stock-lut-needs-log-in-and-a-balance-in-front-of-it
kind: procedure
conflict-key: how-to-get-a-broadcast-film-look-on-rec709-footage
status: live
supersedes: []
verified-on: 2026-09-22
applies-when: display-referred Rec.709 footage (DJI Normal, not D-Log M) needs the film look used in film and broadcast finishing
not-when: the source is already log or a film scan, in which case skip the Cineon conversion and feed the print stock directly
route: set the project timeline AND output to Rec.709 primaries / Cineon Film Log (tools/remote/resolve_render.py --log), measure the LOG image's channel means with no LUT, set CDL Offset per channel to (grey - channel)/255 to neutralise, then CDL Power ~1.12 and Saturation ~1.6 for the film-scan mimic, then the print stock on the same node's LUT. SetCDL runs before the node's LUT, which is the lab order.
sibling: match-a-reference-photos-grade-by-baking-color-matcher-into-a-cube
asked-as:
  - how do I get a cinematic film look for broadcast television
  - my Kodak 2383 grade looks wrong
  - why is my film emulation so blue
  - what is the professional node order for film emulation
---

**A print-stock LUT was built to receive CINEON LOG and it has no opinion about white
balance. Give it display Rec.709, or give it an uncorrected cast, and it will look wrong in
two different ways.**

Confirmed against the field 2026-09-22 ([Blackmagic forum](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=204521),
[Juan Melara](https://juanmelara.com.au/blog/print-film-emulation-luts-for-download)): the
stock Resolve Film Looks expect Cineon log gamma, so a CST to Rec.709 / Cineon Film Log goes
in front of them, and *"the 2383 PFE LUT expects a film scan input, so unless digital footage
is graded to mimic a film scan it will produce less desirable results."*

**The order, and why each step is where it is:**

1. **Timeline and output on Rec.709 / Cineon Film Log.** Colour management puts the clip in log
   before the node; the LUT itself does the log to display step it was designed for.
2. **Balance with CDL OFFSET, not slope.** In log, an offset shifts density -- that is exactly
   what a printer light is. A slope in log is a per-channel gamma. Measured: a closed loop
   correcting balance with slope oscillated to the clamp in two passes, channel means going
   12/58/95 then 202/29/0 then 1/171/230. With offsets, one measurement of the ungraded log
   image solves it: means 83/97/111, offsets +0.053 / +0.001 / -0.054, done.
3. **Power ~1.12 and Saturation ~1.6** are the "mimic a film scan" step the print stock wants.
4. **Print stock last**, on the same node's LUT, because `SetCDL` runs BEFORE the node's LUT.

**What it fixes, measured on clip 0002:** print stock straight onto display Rec.709 with no
balance gave R13 G58 B95 -- a blue disaster that was the print faithfully amplifying an
uncorrected dusk cast. The same stock through this chain gives R52 G61 B68, blacks at 16,
highlights at 185, nothing clipped.

This is the chain [[the-osmo-film-chain-balance-then-cdl-in-log-then-a-print-lut]] describes,
with the balance control corrected from gain to offset and the log conversion made explicit.
