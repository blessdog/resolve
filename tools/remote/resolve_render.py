#!/usr/bin/env python3
"""Runs ON whichever machine has Resolve Studio. One clip, one look, one render or still.

    python3 resolve_render.py <clip> <out_dir> <tag> [--lut PATH] [--cdl R,G,B]
        [--size WxH] [--fps N] [--quality KBPS] [--window A,B] [--still-at S[,S...]]
        [--project NAME] [--retime]

Deliberately dumb: it does no probing and guesses nothing. --size and --fps are
passed in by the caller (tools/render-mini.py), which probed the source. The
remote host needs no repo checkout and no ffmpeg.

The look is one colour node: --cdl sets its ASC CDL slope, which runs BEFORE the
node's LUT, so `--cdl` is the technical balance and `--lut` is the look, in that
order, in one node.

Writer: tools/render-mini.py ships and runs this file. Reader: the pulled-back
mp4 or jpg. **Fails when wrong: a render that comes back ungraded.** That is not
hypothetical — measured 2026-09-21, SetLUT returned False for a LUT in the user
Library (Resolve reads only /Library/Application Support/.../LUT) and the mini
spent 845 s producing an ungraded file, reporting success. So a requested LUT is
read back with GetLUT and a miss exits non-zero BEFORE any render starts.
"""
import os
import sys
import time

API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
DEFAULT_LIB = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"


def running_resolve_lib():
    """fusionscript.so from the bundle that is actually RUNNING.

    A machine can carry more than one Resolve install: measured 2026-09-21, the
    Mac mini has one in /Applications and one on an external SSD at
    /Volumes/BleSSD/Applications/DaVinciResolve. `open -a "DaVinci Resolve"`
    picked the external one while this script loaded the /Applications library,
    and scriptapp() returned False with Resolve plainly running at 700% CPU --
    a failure that looks exactly like the broken-scripting-after-pkill one but
    is only a mismatched bundle.
    """
    import subprocess
    marker = "/DaVinci Resolve.app/Contents/MacOS/"
    out = subprocess.run(["ps", "-Ao", "command="], capture_output=True, text=True).stdout
    for line in out.splitlines():
        i = line.find(marker)
        if i > 0:
            lib = os.path.join(line[:i], "DaVinci Resolve.app",
                               "Contents/Libraries/Fusion/fusionscript.so")
            if os.path.isfile(lib):
                return lib
    return None


os.environ.setdefault("RESOLVE_SCRIPT_API", API)
os.environ.setdefault("RESOLVE_SCRIPT_LIB", running_resolve_lib() or DEFAULT_LIB)
print("scripting library:", os.environ["RESOLVE_SCRIPT_LIB"])
sys.path.append(os.path.join(API, "Modules"))
import DaVinciResolveScript as dvr  # noqa: E402


def flag(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


# Absolute, both of them: ImportMedia returns [] for a relative clip without saying why, and a
# relative TargetDir raises Resolve's modal 'Render Path Inaccessible', which then blocks every
# later script until someone clicks it (measured 2026-09-18).
CLIP = os.path.abspath(os.path.expanduser(sys.argv[1]))
OUT = os.path.abspath(os.path.expanduser(sys.argv[2]))
TAG = sys.argv[3]
LUT = flag("--lut")
CDL = [float(x) for x in flag("--cdl", "1,1,1").split(",")]
W, H = (int(x) for x in flag("--size", "3840x2160").split("x"))
FPS = flag("--fps", "24")
QUALITY = flag("--quality", "60000")
WINDOW = flag("--window")
STILLS = [float(s) for s in flag("--still-at", "").split(",") if s.strip()]
PROJECT = flag("--project", "remote-render")
RETIME = "--retime" in sys.argv

if not os.path.exists(CLIP):
    sys.exit(f"no such clip on this host: {CLIP}")
os.makedirs(OUT, exist_ok=True)

app = dvr.scriptapp("Resolve")
if not app:
    sys.exit("Resolve is not answering. It may be running after a `pkill`, which permanently "
             "breaks scripting; quit it with osascript and `open -a` it again.")
# StopRendering returns at once but Resolve holds a modal until it has finished stopping.
for _ in range(150):
    cur = app.GetProjectManager().GetCurrentProject()
    if app.GetCurrentPage() is not None and not (cur and cur.IsRenderingInProgress()):
        break
    time.sleep(2)
else:
    sys.exit("Resolve stayed busy for 5 minutes (a modal is up, or a render is still stopping)")

pm = app.GetProjectManager()
proj = pm.LoadProject(PROJECT) or pm.CreateProject(PROJECT)
if not proj:
    sys.exit(f"could not open or create project {PROJECT!r}")

# Display-referred source in, display-referred out: the print LUTs and the reference-matched
# cubes were both baked from display Rec.709 frames, so the timeline must not re-encode.
for k, v in (("timelineFrameRate", FPS), ("timelineResolutionWidth", str(W)),
             ("timelineResolutionHeight", str(H)),
             ("colorScienceMode", "davinciYRGBColorManagedv2"),
             ("separateColorSpaceAndGamma", "1"),
             ("colorSpaceTimeline", "Rec.709"), ("colorSpaceTimelineGamma", "Gamma 2.4"),
             ("colorSpaceOutput", "Rec.709"), ("colorSpaceOutputGamma", "Gamma 2.4"),
             ("colorSpaceOutputToneMapping", "None"), ("colorSpaceOutputGamutMapping", "None")):
    proj.SetSettings({k: v})
read = proj.GetSettings()
print("project", PROJECT, {k: read.get(k) for k in ("timelineFrameRate", "timelineResolutionWidth",
                                                    "colorSpaceTimeline", "colorSpaceTimelineGamma")})

mp = proj.GetMediaPool()
items = [c for c in mp.GetRootFolder().GetClipList() if c.GetClipProperty("File Path") == CLIP]
items = items or mp.ImportMedia([CLIP])
if not items:
    sys.exit(f"ImportMedia refused {CLIP}")
for i in range(proj.GetTimelineCount(), 0, -1):
    t = proj.GetTimelineByIndex(i)
    if t and t.GetName() == TAG:
        mp.DeleteTimelines([t])
tl = mp.CreateTimelineFromClips(TAG, [items[0]])
if not tl:
    sys.exit(f"CreateTimelineFromClips refused {TAG}")
proj.SetCurrentTimeline(tl)
ti = tl.GetItemListInTrack("video", 1)[0]

if RETIME:
    ti.SetProperty("RetimeProcess", 3)        # optical flow
    ti.SetProperty("MotionEstimation", 5)     # Speed Warp
if CDL != [1.0, 1.0, 1.0]:
    ok = ti.SetCDL({"NodeIndex": "1", "Slope": f"{CDL[0]} {CDL[1]} {CDL[2]}",
                    "Offset": "0 0 0", "Power": "1 1 1", "Saturation": "1"})
    print("cdl slope", CDL, "->", ok)
    if not ok:
        sys.exit("SetCDL refused the balance; the render would be unbalanced")
if LUT:
    g = ti.GetNodeGraph()
    ok = g.SetLUT(1, LUT)
    back = g.GetLUT(1)
    print("lut", LUT, "-> set", ok, "reads", repr(back))
    # The readback, not the boolean, is the test. See this file's docstring.
    if not back:
        sys.exit(f"LUT {LUT!r} did not stick. Resolve reads only "
                 f"'/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT'; "
                 f"a copy in the user Library is invisible to it. Refusing to render ungraded.")

start, end = tl.GetStartFrame(), tl.GetEndFrame()
print("frames", end - start, "fps", read.get("timelineFrameRate"))

if STILLS:
    gallery = proj.GetGallery()
    album = gallery.GetCurrentStillAlbum()
    fps_f = float(read.get("timelineFrameRate") or FPS)
    for sec in STILLS:
        f = start + int(round(sec * fps_f))
        tc_f = f % int(round(fps_f))
        tc_s = f // int(round(fps_f))
        tl.SetCurrentTimecode(f"{tc_s // 3600:02d}:{tc_s % 3600 // 60:02d}:{tc_s % 60:02d}:{tc_f:02d}")
        still = tl.GrabStill()
        if not still:
            sys.exit(f"GrabStill refused at {sec}s")
        album.ExportStills([still], OUT, f"{TAG}-{sec:g}s", "jpg")
        print("still", sec, "->", OUT)
    album.DeleteStills(album.GetStills())
    pm.SaveProject()
    raise SystemExit(0)

app.OpenPage("deliver")
proj.SetCurrentRenderFormatAndCodec("mp4", "H265")
settings = {"TargetDir": OUT, "CustomName": TAG, "FormatWidth": W, "FormatHeight": H,
            "VideoQuality": int(QUALITY), "EncodingProfile": "Main10",
            "ExportVideo": True, "ExportAudio": False,
            "ColorSpaceTag": "Rec.709", "GammaTag": "Gamma 2.4"}
if WINDOW:
    a, b = (float(x) for x in WINDOW.split(","))
    fps_f = float(read.get("timelineFrameRate") or FPS)
    settings.update({"SelectAllFrames": False,
                     "MarkIn": start + int(round(a * fps_f)),
                     "MarkOut": start + int(round(b * fps_f))})
else:
    settings["SelectAllFrames"] = True
print("render settings ->", proj.SetRenderSettings(settings))
job = proj.AddRenderJob()
if not job:
    sys.exit("AddRenderJob refused")
t0 = time.time()
proj.StartRendering([job], False)
while proj.IsRenderingInProgress():
    time.sleep(3)
elapsed = time.time() - t0
status = proj.GetRenderJobStatus(job) or {}
print("status", status.get("JobStatus"), f"{elapsed:.0f}s")
pm.SaveProject()
if status.get("JobStatus") != "Complete":
    sys.exit(f"render did not complete: {status}")
