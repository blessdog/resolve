#!/usr/bin/env python3
"""Matches a clip's colour to a REFERENCE PHOTO Ryan likes, and bakes the match into a
3D LUT that Resolve applies to the whole clip.

Ryan, 2026-09-19: "Would you be able to match color grading from photos that I like the
color grading on?" Yes, and it is a solved problem class: statistical colour transfer,
Reinhard 2001 and Pitie's Monge-Kantorovich linear (MKL) transform.

PRIOR ART: the transfer itself is `color-matcher` (hahnec/color-matcher, PyPI 0.6.0,
methods mkl / reinhard / hm / mvgd / hm-mkl-hm). Nothing here re-implements it. This file
does the two things that library does not: it RECOVERS the fitted transform so it can be
applied to points the reference never contained, and it writes the result as a .cube.

Why a LUT and not just the transferred frame: `color-matcher` maps one image to another.
A film needs the same mapping on every frame, so the fitted transform is applied to an
identity lattice and written as a 33^3 .cube, which Resolve puts on colour node 1 through
the same SetLUT call the print stocks use.

How the transform is recovered: MKL and Reinhard are AFFINE in RGB, so running the library
on the frame and solving least-squares for the 3x4 matrix that maps source pixels to result
pixels recovers the fit exactly. The residual is printed; if it is not near zero the method
was not affine (hist matching is not) and the tool falls back to per-channel curves.

    python3 match_reference.py <reference.jpg> <source-frame.png> <out.cube>
                               [--method mkl|reinhard|hm-mkl-hm] [--strength 0-1] [--size 33]

Writer: this file. Reader: dctl_film_mini.py --print-lut, and Resolve's LUT folder.
Fails when wrong: the residual line prints a large number, which means the baked LUT does
not reproduce the library's own result and must not be trusted.
"""
import os
import sys

import numpy as np
from PIL import Image
from color_matcher import ColorMatcher


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


REF, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
METHOD = arg("--method", "mkl")
STRENGTH = float(arg("--strength", "1.0"))
N = int(arg("--size", "33"))


def load(path, longest=900):
    im = Image.open(path).convert("RGB")
    im.thumbnail((longest, longest), Image.LANCZOS)   # statistics, not detail
    return np.asarray(im).astype(np.float64) / 255.0


ref, src = load(REF), load(SRC)
res = ColorMatcher(src=src, ref=ref, method=METHOD).main()
res = np.clip(np.asarray(res, dtype=np.float64), 0.0, 1.0)
if res.max() > 1.5:                                    # some methods return 0-255
    res = res / 255.0

s = src.reshape(-1, 3)
r = res.reshape(-1, 3)
A = np.hstack([s, np.ones((len(s), 1))])               # affine: [R G B 1] -> [R G B]
M, *_ = np.linalg.lstsq(A, r, rcond=None)
resid = float(np.abs(A @ M - r).mean())
print(f"method {METHOD}  affine residual {resid:.5f} display codes/255 "
      f"({resid * 255:.2f} codes)")
AFFINE = resid < 0.01
if not AFFINE:
    print("  not affine; falling back to per-channel curves fitted from the same result")
    curves = []
    for c in range(3):
        order = np.argsort(s[:, c])
        xs, ys = s[order, c], r[order, c]
        edges = np.linspace(0, 1, 256)
        idx = np.searchsorted(xs, edges)
        idx = np.clip(idx, 0, len(ys) - 1)
        k = 9
        sm = np.convolve(ys[idx], np.ones(k) / k, mode="same")
        sm[:k] = ys[idx][:k]
        sm[-k:] = ys[idx][-k:]
        curves.append((edges, np.clip(sm, 0, 1)))

g = np.linspace(0.0, 1.0, N)
lattice = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1).reshape(-1, 3)
lattice = lattice[:, ::-1].copy()                      # .cube order: red fastest
if AFFINE:
    out = np.hstack([lattice, np.ones((len(lattice), 1))]) @ M
else:
    out = np.stack([np.interp(lattice[:, c], curves[c][0], curves[c][1]) for c in range(3)], 1)
out = lattice + STRENGTH * (out - lattice)
out = np.clip(out, 0.0, 1.0)

os.makedirs(os.path.dirname(os.path.abspath(OUT)) or ".", exist_ok=True)
with open(OUT, "w") as f:
    f.write(f"# matched to {os.path.basename(REF)} from {os.path.basename(SRC)}\n")
    f.write(f"# color-matcher method {METHOD}, strength {STRENGTH}, affine {AFFINE}\n")
    f.write(f'TITLE "match-{os.path.splitext(os.path.basename(REF))[0]}-{METHOD}"\n')
    f.write(f"LUT_3D_SIZE {N}\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
    for v in out:
        f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
print(f"wrote {OUT}  ({N}^3 = {len(out)} entries)")

# what the match actually does to the frame, so the claim is checkable
def stats(a):
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0).mean() * 100
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    return sat, np.percentile(y, 1) * 255, np.percentile(y, 99) * 255, [round(a[..., c].mean() * 255) for c in range(3)]
for lab, a in (("reference", ref), ("source", src), ("matched", res)):
    st = stats(a)
    print(f"  {lab:10s} colour {st[0]:5.1f}%  blacks {st[1]:5.0f}  whites {st[2]:5.0f}  RGB {st[3]}")
