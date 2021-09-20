import vapoursynth as vs
core = vs.core

import os
import random
import havsfunc as hvf
import mvsfunc as mvf
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
import insaneAA
import vsTAAmbk as taa
from adptvgrnMod import adptvgrnMod as agmod
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth
import vscompare
import atomchtools as atf
from cooldegrain import CoolDegrain
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth, get_w

def compac(src, enc):
    for i in [4000, 5754, 12355, 15689, 15924, 19063, 24000]:
        frame = i
        src, enc = vscompare.prep(src, enc, w=1920, h=1080, dith=True, yuv444=False)
        vscompare.save(frame, src=src, enc=enc)

key = key.decode() #"[SubsPlease] Heike Monogatari - 01 (1080p) [516659CC].mkv" 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source)
h = 886 # not necessarily this resolution. But shows less error at this, so decided to extract edge from this
w = get_w(h)
src = core.std.AssumeFPS(src, fpsnum = 24000, fpsden = 1001)
src = src.resize.Spline36(range_in_s="full", range_s="limited")
src = depth(src, 16)
    
b = 1/3
c = 1/3

rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=h, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3)), 16)
upscale = join([rescale, plane(src, 1), plane(src, 2)])

# src.set_output(0)
# upscale.set_output(1)

line_mask = kgf.retinex_edgemask(upscale).std.Binarize(16000).rgvs.RemoveGrain(3)
line_mask = line_mask.std.Minimum()

# kgf.retinex_edgemask(upscale).std.Binarize(9999).rgvs.RemoveGrain(3).set_output(3)
# line_mask.set_output(2)

dehalo = core.std.MaskedMerge(src, upscale, line_mask)
dehalo = join([dehalo, plane(src, 1), plane(src, 2)])

# dehalo.set_output(3)

#hvf.DeHalo_alpha(dehalo, darkstr=0.3, brightstr=0).set_output(4)
# core.f3kdb.Deband(

dehalo = hvf.DeHalo_alpha(dehalo, darkstr=0.2, brightstr=1)     #, range=16, y=32, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True).set_output(5)
ref = hvf.SMDegrain(dehalo, tr=1, thSAD=64, plane=4)
denoise = mvf.BM3D(dehalo, sigma=[0.8, 0.2], ref=ref)
# denoise.set_output(1)

deband = core.f3kdb.Deband(denoise, range=16, y=32, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
grain = kgf.adaptive_grain(deband, 0.30, luma_scaling=8)

# compac(src, grain)

final = depth(grain, 10)
final.set_output()
