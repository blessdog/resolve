#!/bin/sh
# Start Resolve on the mini, run a render job, QUIT IT AGAIN.
#
# Resolve on the mini does not idle: measured twice, 2026-09-22 and 2026-09-23, it sits at
# ~700-750% CPU indefinitely after a render batch and stops answering both scripting and
# AppleEvents. The second time it burned 17 h 44 m of an 8 GB machine Ryan was trying to
# work on. So the lifetime of Resolve on that box is the lifetime of the JOB, never longer.
#
#   ./mini_session.sh "<command to run on the mini, resolve_render.py ...>"
#
# Writer: this file. Reader: whoever offloads a render. Fails when wrong: the mini is left
# with a spinning Resolve eating its RAM, which is what this exists to prevent.
set -e
APP="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve"

cleanup() {
  osascript -e 'quit app "DaVinci Resolve"' >/dev/null 2>&1 || true
  sleep 10
  pkill -9 -f "DaVinci Resolve" >/dev/null 2>&1 || true
  echo "resolve stopped, $(ps -Ao command= | grep -c '[D]aVinci Resolve') left"
}
trap cleanup EXIT INT TERM

pkill -9 -f "DaVinci Resolve" >/dev/null 2>&1 || true
sleep 4
nohup "$APP" -nogui >/tmp/resolve-nogui.log 2>&1 &
# Headless, because with no GUI session there is no invisible modal to hang on and
# StopRendering returns clean instead of blocking.

i=0
while [ $i -lt 30 ]; do
  sleep 5
  if /usr/bin/python3 - <<'PY' 2>/dev/null
import os, sys
API = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
os.environ.setdefault("RESOLVE_SCRIPT_API", API)
os.environ.setdefault("RESOLVE_SCRIPT_LIB",
                      "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so")
sys.path.append(API + "/Modules")
import DaVinciResolveScript as dvr
a = dvr.scriptapp("Resolve")
sys.exit(0 if (a and a.GetCurrentPage() is not None) else 1)
PY
  then echo "resolve up after $((i*5+5))s"; break; fi
  i=$((i+1))
done

sh -c "$1"
