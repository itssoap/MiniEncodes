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

key = "Star.Wars.Visions.S01E01.The.Duel.1080p.DSNP.WEB-DL.DDP5.1.H.264-FLUX.mkv" #key.decode() 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1000)
src = depth(src, 16)

# Crop the black bars

# bg = core.std.BlankClip(color=(255, 128, 128), width=1920, height=1080, fpsnum=24000, fpsden=1001, length=18368, format=vs.YUV420P16)
crop = core.std.Crop(src, 0, 0, 132, 132)
crop1 = crop[739:18120]
# src.set_output(0)
# crop1.set_output(1)
# bg.set_output(2)

denoise = core.knlm.KNLMeansCL(crop1, d=2, s=2, h=1.0, device_type='auto')
denoise = core.std.MaskedMerge(crop1, denoise, kgf.retinex_edgemask(denoise))

deband = core.f3kdb.Deband(denoise, range=16, y=32, cb=8, cr=8, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
grain = kgf.adaptive_grain(crop[:739]+deband[739:18120]+crop[18120:], strength=0.30, luma_scaling=12)

final = depth(grain, 10)
final.set_output()
