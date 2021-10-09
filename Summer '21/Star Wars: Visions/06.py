import vapoursynth as vs
core = vs.core
core.max_cache_size = 8*2**10
core.num_threads = 4

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
import debandshit as dbs
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth, get_w

key = "Star.Wars.Visions.S01E06.T0-B1.1080p.DSNP.WEB-DL.DDP5.1.H.264-FLUX.mkv" #key.decode() 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1000)
src = depth(src, 16)

# Crop the black bars

# bg = core.std.BlankClip(color=(255, 128, 128), width=1920, height=1080, fpsnum=24000, fpsden=1001, length=18368, format=vs.YUV420P16)
semicrop = core.std.Crop(src, 0, 0, 132, 132)
# semicrop.set_output(0)
crop = semicrop[520:18528]

aa = lvf.aa.transpose_aa(crop, eedi3=False, rep=3)
# src.set_output(0)
# crop.set_output(1)
# aa.set_output(2)

dehalo = hvf.DeHalo_alpha(aa, rx=1.2, darkstr=0.4, brightstr=1.0)
# dehalo.set_output(3)

ref = hvf.SMDegrain(dehalo, tr=1, thSAD=32, plane=4)
denoise = mvf.BM3D(dehalo, sigma=[0.6, 0.2], ref=ref)

deband = core.f3kdb.Deband(denoise, range=18, y=128, cb=32, cr=32, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
# deband.set_output(4)

grain = agmod(semicrop[:520]+deband+semicrop[18528:], strength=0.6, size=0.5, static=True, luma_scaling=8)
# grain.set_output(5)

final = depth(grain, 10)
final.set_output()
