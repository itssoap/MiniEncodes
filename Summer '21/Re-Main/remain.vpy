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
h = 844
w = get_w(h)
src = core.std.AssumeFPS(src, fpsnum = 24000, fpsden = 1001)
src = src.resize.Spline36(range_in_s="full", range_s="limited")
src = depth(src, 16)
    
b = 1/3
c = 1/3
descale = depth(lvf.scale.descale(clip=src, upscaler=None, height=h, kernel=lvf.kernels.Bicubic(b=b, c=c)), 16)
aa = taa.TAAmbk(descale, aatype='Nnedi3')
upscale = nnedi3_rpow2(aa).resize.Spline36(src.width, src.height)
upscale = join([upscale, plane(src, 1), plane(src, 2)])
upscale = depth(upscale, 16)
    
ref = hvf.SMDegrain(upscale, tr=1, thSAD=64, plane=4)
denoise = mvf.BM3D(upscale, sigma=[3.4, 1.2], ref=ref)

line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = core.f3kdb.Deband(denoise, range=18, y=48, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
deband = core.std.MaskedMerge(deband, upscale, line_mask)
    
grain = kgf.adaptive_grain(deband, 0.20, luma_scaling=8)

final = fvf.Depth(grain, 10)
final.set_output()
