import vapoursynth as vs
core = vs.core
core.max_cache_size = 32*2**10

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

key = key.decode() 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)
# src.set_output(0)
src = src.resize.Spline36(range_in_s="full", range_s="limited")

aa = lvf.aa.transpose_aa(src, eedi3=False, rep=3)
aa = join([aa, plane(src, 1), plane(src, 2)])
# aa.set_output(2)

dehalo = hvf.DeHalo_alpha(aa, rx=1.8, darkstr=0.1, brightstr=1.0)

ref = hvf.SMDegrain(dehalo, tr=1, thSAD=64, plane=4)
denoise = mvf.BM3D(dehalo, sigma=[0.6, 0.2], ref=ref)

deband = core.neo_f3kdb.Deband(dehalo, range=16, y=32, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
# deband.set_output(3)

grain = agmod(deband, strength=1.0, size=0.5, static=True, luma_scaling=6)
# grain = agmod(deband, strength=1.0, size=0.5, static=True, luma_scaling=6)
# grain.set_output(4)

final = depth(grain, 10)
final.set_output()
