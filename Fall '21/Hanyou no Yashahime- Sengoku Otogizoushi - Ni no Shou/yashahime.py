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
import debandshit as dbs
import atomchtools as atf
from cooldegrain import CoolDegrain
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth, get_w

def compac(src, enc):
    for i in [4000, 5754, 12355, 15689, 15924, 19063, 24000]:
        frame = i
        src, enc = vscompare.prep(src, enc, w=1920, h=1080, dith=True, yuv444=False)
        vscompare.save(frame, src=src, enc=enc)

key = key.decode()
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)
h = 810
w = get_w(h)
src = core.std.AssumeFPS(src, fpsnum = 24000, fpsden = 1001)
src = depth(src, 16)
b = 1/3
c = 1/3

rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=h, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3)), 16)
upscale = join([rescale, plane(src, 1), plane(src, 2)])

# src.set_output(0)
# upscale.set_output(1)
dehalo = hvf.DeHalo_alpha(upscale, rx=1.8, darkstr=0.4, brightstr=1)
# dehalo.set_output(2)

ref = hvf.SMDegrain(dehalo, tr=1, thSAD=64, plane=4)
denoise = mvf.BM3D(dehalo, sigma=[1.2, 1.0], ref=ref)

# denoise.set_output(3)

deband = core.f3kdb.Deband(denoise, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
grain = agmod(deband, strength=0.5, size=0.75, static=True, luma_scaling=8)

final = depth(grain, 10)
final.set_output()
