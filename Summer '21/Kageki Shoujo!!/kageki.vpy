import vapoursynth as vs
import os
import sys
import subprocess
from typing import NamedTuple

import havsfunc as hvf
import mvsfunc as mvf
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth, get_w

core = vs.core
core.max_cache_size = 18000

key = key.decode()
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source)
src = core.std.AssumeFPS(src, fpsnum = 24000, fpsden = 1001)
src = src.resize.Spline36(range_in_s="full", range_s="limited")
src = depth(src, 16)
    
Y, U, V = kgf.split(src)
Y = depth(Y, 16)

# AA
luma_aa = taa.TAAmbk(Y, aatype='Nnedi3')

ref = hvf.SMDegrain(luma_aa, tr=1, thSAD=128, plane=4)
denoise = mvf.BM3D(luma_aa, sigma=[1.8, 0.6, 0], ref=ref)

remerge = kgf.join([denoise, U, V])

line_mask = kgf.retinex_edgemask(remerge).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = core.f3kdb.Deband(remerge, range=18, y=32, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
deband = core.std.MaskedMerge(deband, remerge, line_mask)
    
grain = kgf.adaptive_grain(deband, 0.30, luma_scaling=8)

final = fvf.Depth(grain, 10)
final.set_output()
