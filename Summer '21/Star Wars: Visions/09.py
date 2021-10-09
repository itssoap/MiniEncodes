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

key = "Star.Wars.Visions.S01E09.Akakiri.1080p.DSNP.WEB-DL.DDP5.1.H.264-FLUX.mkv" #key.decode() 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1000)
src = depth(src, 16)

# Crop the black bars

# bg = core.std.BlankClip(color=(255, 128, 128), width=1920, height=1080, fpsnum=24000, fpsden=1001, length=18368, format=vs.YUV420P16)
semicrop = core.std.Crop(src, 0, 0, 132, 132)
crop = semicrop[511:18096]
# src.set_output(0)
# crop.set_output(1)
# bg.set_output(2)

aa = lvf.aa.transpose_aa(crop, eedi3=False, rep=4)
# aa.set_output(2)

# aa1 = lvf.aa.transpose_aa(crop, eedi3=False, rep=8)
# aa1.set_output(3)

ref = hvf.SMDegrain(aa, tr=1, thSAD=32, plane=4)
denoise = mvf.BM3D(aa, sigma=[0.8, 0.2], ref=ref)

deband = core.f3kdb.Deband(denoise, range=18, y=64, cb=32, cr=32, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
# deband.set_output(4)

grain = agmod(semicrop[:511]+deband+semicrop[18096:], strength=0.3, size=0.5, static=True, luma_scaling=10)
# grain.set_output(4)

final = depth(grain, 10)
final.set_output()
