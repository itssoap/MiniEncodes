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

def compac(src, enc):
    for i in [4000, 5754, 12355, 15689, 15924, 19063, 24000]:
        frame = i
        src, enc = vscompare.prep(src, enc, w=1920, h=1080, dith=True, yuv444=False)
        vscompare.save(frame, src=src, enc=enc)

key = key.decode() #"[SubsPlease] Takt Op. Destiny - 01 (1080p) [DB124E70].mkv" #key.decode()
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)
src = core.std.AssumeFPS(src, fpsnum = 24000, fpsden = 1001)
src = depth(src, 16)

aa = lvf.aa.transpose_aa(src, eedi3=False, rep=3)
aa = join([aa, plane(src, 1), plane(src, 2)])
# src.set_output(0)
# aa.set_output(1)

line_mask = kgf.retinex_edgemask(aa).std.Binarize(16000).rgvs.RemoveGrain(3)
line_mask = line_mask.std.Minimum()
# line_mask.set_output(2)

dehalo = core.std.MaskedMerge(src, aa, line_mask)
dehalo = join([dehalo, plane(src, 1), plane(src, 2)])
# dehalo.set_output(3)

ref = hvf.SMDegrain(dehalo, tr=1, thSAD=32, plane=4)
denoise = mvf.BM3D(dehalo, sigma=[1.0, 0.2], ref=ref)
# denoise.set_output(4)

deband = core.f3kdb.Deband(denoise, range=16, y=32, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
grain = agmod(deband, strength=0.30, size=0.5, luma_scaling=8)
# grain.set_output(5)

final = depth(grain, 10)
final.set_output()
