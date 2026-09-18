#!/usr/bin/env python3
"""Solves the per-clip BALANCE stage: the channel gains that make a frame neutral, measured
in Resolve's own pipeline rather than guessed from an ffmpeg frame.

Ryan, 2026-09-18, on the node order a colourist uses: "Node 1: fix exposure and white
balance. Don't make the look here." A look laid over an unbalanced shot spends its whole
range fighting the cast, which is why every emulation on Osmo clip 0002 read murky: the
frame was blue by 30 display codes (R 105, G 121, B 135) before any grade touched it.

Closed loop, because the comp runs scene-linear and a display-code ratio is not a linear
gain: set gains, export a still, measure its channel means, correct, repeat. Converges in
three or four passes. The solved gains are written into a recipe in dctl-film-recipes.json
so every later render uses them.

    python3 auto_balance.py <clip> <tag> <recipe-name> [--at S] [--fps N] [--timeline MODE]
                            [--target-mid 0.45] [--iters 4]

Writer: this file. Reader: dctl_film_mini.py, which runs the recipe it writes.
Fails when wrong: the balance recipe's gains stop making the frame neutral, which shows up
as a colour cast in every look built on top of it.
"""
import json
import os
import sys
import time

import numpy as np
from PIL import Image

API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
os.environ.setdefault("RESOLVE_SCRIPT_API", API)
os.environ.setdefault("RESOLVE_SCRIPT_LIB",
                      "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so")
sys.path.append(os.path.join(API, "Modules"))
import DaVinciResolveScript as dvr  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RECIPES = os.path.join(HERE, "dctl-film-recipes.json")


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


CLIP = os.path.abspath(sys.argv[1])
TAG, RECIPE = sys.argv[2], sys.argv[3]
AT = float(arg("--at", "5"))
FPS = arg("--fps", "25")
TIMELINE = arg("--timeline", "rec709")
TARGET_MID = float(arg("--target-mid", "0.45"))   # where the frame's median should land, 0-1
ITERS = int(arg("--iters", "4"))
SCRATCH = os.path.join("/private/tmp", f"balance-{TAG}")
os.makedirs(SCRATCH, exist_ok=True)

COLOUR = {"rec709": [("colorSpaceTimeline", "Rec.709"), ("colorSpaceTimelineGamma", "Gamma 2.4"),
                     ("colorSpaceOutput", "Rec.709"), ("colorSpaceOutputGamma", "Gamma 2.4")],
          "linear": [("colorSpaceTimeline", "Rec.709"), ("colorSpaceTimelineGamma", "Linear"),
                     ("colorSpaceOutput", "Rec.709"), ("colorSpaceOutputGamma", "Gamma 2.4")],
          "cineon": [("colorSpaceTimeline", "Rec.709"), ("colorSpaceTimelineGamma", "Cineon Film Log"),
                     ("colorSpaceOutput", "Rec.709"), ("colorSpaceOutputGamma", "Cineon Film Log")]}[TIMELINE]

app = dvr.scriptapp("Resolve")
if not app:
    sys.exit("Resolve is not answering")
if app.GetCurrentPage() is None:
    sys.exit("a modal dialog holds Resolve; every measurement from this session would be void")
pm = app.GetProjectManager()
name = f"{TAG}-balance"
proj = pm.LoadProject(name) or pm.CreateProject(name)
for k, v in [("timelineFrameRate", FPS), ("colorScienceMode", "davinciYRGBColorManagedv2"),
             ("separateColorSpaceAndGamma", "1"), ("colorSpaceOutputToneMapping", "None"),
             ("colorSpaceOutputGamutMapping", "None"), *COLOUR]:
    proj.SetSettings({k: v})
mp = proj.GetMediaPool()
items = [c for c in mp.GetRootFolder().GetClipList() if c.GetClipProperty("File Path") == CLIP] or mp.ImportMedia([CLIP])
item = items[0]
w, h = (int(v) for v in str(item.GetClipProperty("Resolution")).split("x"))
proj.SetSettings({"timelineResolutionWidth": str(w), "timelineResolutionHeight": str(h)})
for i in range(proj.GetTimelineCount(), 0, -1):
    t = proj.GetTimelineByIndex(i)
    if t.GetName() == "balance":
        mp.DeleteTimelines([t])
tl = mp.CreateTimelineFromClips("balance", [item])
proj.SetCurrentTimeline(tl)
ti = tl.GetItemListInTrack("video", 1)[0]
comp = ti.GetFusionCompByIndex(1) if ti.GetFusionCompCount() else ti.AddFusionComp()
reg = {t.GetAttrs("TOOLS_RegID"): t for t in comp.GetToolList(False).values()}
for t in comp.GetToolList(False).values():
    if t.GetAttrs("TOOLS_RegID") == "ColorGain":
        t.Delete()
cg = comp.AddTool("ColorGain")
cg.SetAttrs({"TOOLS_Name": "s1_balance"})
cg.ConnectInput("Input", reg["MediaIn"])
reg["MediaOut"].ConnectInput("Input", cg)

nominal = round(float(FPS))
f = tl.GetStartFrame() + round(AT * float(FPS))
tc = f"{f // (3600 * nominal):02d}:{f // (60 * nominal) % 60:02d}:{f // nominal % 60:02d}:{f % nominal:02d}"
app.OpenPage("color")


def measure(gains, i):
    for ch, g in zip("RedGreenBlue".replace("Green", "|Green|").split("|"), gains):
        pass
    cg.SetInput("GainRed", float(gains[0])); cg.SetInput("GainGreen", float(gains[1])); cg.SetInput("GainBlue", float(gains[2]))
    tl.SetCurrentTimecode(tc)
    time.sleep(3)
    path = os.path.join(SCRATCH, f"iter{i}.png")
    if not proj.ExportCurrentFrameAsStill(path):
        sys.exit("ExportCurrentFrameAsStill failed")
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255.0
    return a, [float(a[..., c].mean()) for c in range(3)], float(np.median(a.mean(axis=2)))


gains = [1.0, 1.0, 1.0]
for i in range(ITERS):
    a, means, mid = measure(gains, i)
    grey = sum(means) / 3.0
    cast = (max(means) - min(means)) * 255
    print(f"pass {i}: gains {[round(g,3) for g in gains]}  channel means {[round(m*255) for m in means]}  "
          f"cast {cast:.1f} codes  median {mid*255:.0f}")
    if cast < 1.5 and abs(mid - TARGET_MID) < 0.02:
        print("converged")
        break
    # display-code ratio -> linear gain. Damped so a bright or dark subject cannot run it away.
    for c in range(3):
        ratio = (grey / means[c]) if means[c] > 1e-4 else 1.0
        gains[c] *= float(np.clip(ratio, 0.5, 2.0)) ** (2.4 * 0.8)
    exp = float(np.clip(TARGET_MID / max(mid, 1e-4), 0.5, 2.0)) ** (2.4 * 0.6)
    gains = [g * exp for g in gains]

a, means, mid = measure(gains, ITERS)
print(f"final : gains {[round(g,4) for g in gains]}  channel means {[round(m*255) for m in means]}  "
      f"cast {(max(means)-min(means))*255:.1f} codes  median {mid*255:.0f}")

book = json.load(open(RECIPES))
book["recipes"][RECIPE] = {
    "why": (f"Solved BALANCE for {os.path.basename(CLIP)} at {AT:g} s by auto_balance.py: channel gains that "
            f"make the frame neutral and land its median at {TARGET_MID:g}, measured inside Resolve on a "
            f"{TIMELINE} timeline. Ryan's node order, 2026-09-18: balance first, look second."),
    "stages": [{"tool": "ColorGain", "role": "balance",
                "inputs": {"GainRed": round(gains[0], 4), "GainGreen": round(gains[1], 4), "GainBlue": round(gains[2], 4)}}]}
json.dump(book, open(RECIPES, "w"), indent=2)
print(f"wrote recipe {RECIPE!r} to {RECIPES}")
pm.SaveProject()
