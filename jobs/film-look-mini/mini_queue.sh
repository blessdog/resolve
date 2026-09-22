#!/bin/sh
# Renders every staged clip with Ryan's pick (2026-09-22): the LIGHTER matched look,
# brightness left exactly as shot. Waits for each clip to finish streaming from the
# MacBook before touching it, so a half-downloaded file can never reach Resolve.
SRC=/Volumes/BleSSD/render/src
OUT=/Volumes/BleSSD/render/out
LUT="film-look/matched/match-fashion-hm-mkl-hm-0.75.cube"
mkdir -p "$OUT"

wait_for() {   # $1 file, $2 expected bytes
  while :; do
    n=$(stat -f%z "$SRC/$1" 2>/dev/null || echo 0)
    [ "$n" = "$2" ] && return 0
    sleep 20
  done
}

render() {     # $1 file, $2 bytes, $3 tag, $4 fps, $5 project
  wait_for "$1" "$2"
  echo "=== $3  $(date +%H:%M:%S)"
  /usr/bin/python3 "$HOME/render/resolve_render.py" "$SRC/$1" "$OUT" "$3" \
    --size 3840x2160 --fps "$4" --quality 80000 --project "$5" --lut "$LUT"
}

render DJI_20260921184748_0002_D.MP4 9662247370  c0002-lighter 25    ride-mini-25
render DJI_20260921190207_0003_D.MP4 32484413    c0003-lighter 29.97 ride-mini-2997
render DJI_20260921190223_0004_D.MP4 8117693133  c0004-lighter 25    ride-mini-25
render DJI_20260921191535_0005_D.MP4 13483012132 c0005-lighter 29.97 ride-mini-2997
echo "=== ALL FOUR DONE ON THE MINI  $(date +%H:%M:%S)"
