---
id: i-kept-tuning-film-look-creator-after-it-had-already-been-rejected
kind: law
conflict-key: what-to-do-when-a-look-is-rejected
status: live
verified-on: 2026-09-18
asked-as:
  - Ryan says the grade looks flat
  - the look was rejected, what now
  - when to stop tuning a plugin and change tools
---

Ryan, 2026-09-18, on three rounds of Film Look Creator variants:

> "These color gradings just look flat. It's like you're reducing the color instead of
> making it... more vibrant. Did you even research anything? You didn't? ... You're just
> doing the same thing we've been doing."

And after a fourth round: *"those suck ass as well, whatever you're doing, uh still is not working."*

**The measurement he was right about, and which was sitting in my own table unremarked:**
saturation as shot 26.8, Film Look Creator restrained 25.8, its Cinematic preset 24.0. Two of
the three looks REDUCED colour. The number was printed, labelled, and reported neutrally
instead of read.

**Two failures, and the second is the one that costs.**
1. Reporting a number without reading it. A measurement in a table nobody interprets is
   decoration. If a column moves the wrong way against what was asked for, say so in the
   sentence, not the table.
2. Research that never reaches the pixels is not research. spektrafilm was found, priced,
   recommended and written into the README in the same session where every render he was
   shown still came from Film Look Creator and a Kodak print LUT, the two tools that had
   already failed. **Installing the new tool and then not rendering with it is the same
   failure as never finding it.**

The rule: **when a look is rejected, the next render must come from a different tool, not a
different parameter.** `stagnation_gate.py` blocks the third parameter pass on one tool in a
turn for exactly this reason, and the spirit of it applies across turns too.

Related: [[name-the-technique-before-the-tool]], [[search-before-you-build]],
[[spektrafilm-installs-without-admin-but-its-menus-are-invisible-to-scripting]].
