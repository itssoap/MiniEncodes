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

key = "Star.Wars.Visions.S01E02.Tatooine.Rhapsody.1080p.DSNP.WEB-DL.DDP5.1.H.264-FLUX.mkv" #key.decode() 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1000)
src = depth(src, 16)

# Crop the black bars

# bg = core.std.BlankClip(color=(255, 128, 128), width=1920, height=1080, fpsnum=24000, fpsden=1001, length=18368, format=vs.YUV420P16)
semicrop = core.std.Crop(src, 0, 0, 132, 132)
crop = semicrop[548:17768]
# src.set_output(0)
# crop.set_output(1)
# dehalo = crop# hvf.DeHalo_alpha(crop, darkstr = 0.2, brightstr=0.8)
# dehalo.set_output(2)

aa = lvf.aa.transpose_aa(crop, eedi3=False, rep=2)
aa = join([aa, plane(crop, 1), plane(crop, 2)])
# aa.set_output(3)
dehalo = hvf.DeHalo_alpha(aa, darkstr = 0.2, brightstr=0.8) #.set_output(4)
#hvf.DeHalo_alpha(aa, darkstr = 1.2, brightstr=1.4).set_output(5)
# dehalo.set_output(2)
degrain = CoolDegrain(dehalo, tr=1.0, thsad=5, thsadc=3)
# degrain.set_output(3)

deband = core.f3kdb.Deband(degrain, range=14, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
# deband.set_output(4)

grain = agmod(semicrop[:548]+deband+semicrop[17768:], strength=0.50, size=0.75, static=True, luma_scaling=6)
# grain.set_output(5)

final = depth(grain, 10)
final.set_output()
