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

key = "Star.Wars.Visions.S01E07.The.Elder.1080p.DSNP.WEB-DL.DDP5.1.H.264-FLUX.mkv" #key.decode() 
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source, force_lsmas=True)

src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1000)
src = depth(src, 16)

# Crop the black bars

# bg = core.std.BlankClip(color=(255, 128, 128), width=1920, height=1080, fpsnum=24000, fpsden=1001, length=18368, format=vs.YUV420P16)
semicrop = core.std.Crop(src, 0, 0, 132, 132)
crop = semicrop[551:22112]
semicrop.set_output(0)
# crop.set_output(1)
# bg.set_output(2)
aa = lvf.aa.transpose_aa(crop, eedi3=False, rep=2)
aa = join([aa, plane(crop, 1), plane(crop, 2)])
# aa.set_output(2)

dehalo = hvf.DeHalo_alpha(aa, rx=1.8, darkstr=0.5, brightstr=0.8)
# dehalo.set_output(3)

halo_mask = lvf.mask.halo_mask(aa, brz=0.3, rad=1)
# halo_mask.set_output(4)

dehalo1 = core.std.MaskedMerge(aa, dehalo, halo_mask)
# dehalo1.set_output(5)
# clean = core.tmc.TMaskCleaner(halo_mask, length=10, thresh=160, fade=0)
# clean.set_output(6)
line_mask = kgf.retinex_edgemask(dehalo1).std.Binarize(11000).rgvs.RemoveGrain(3).std.Deflate().std.Deflate().std.Minimum()
# line_mask.set_output(6)
deband = core.neo_f3kdb.Deband(dehalo1, range=18, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
# deband.set_output(7)
deband = core.std.MaskedMerge(deband, dehalo1, line_mask)
# deband.set_output(7)

grain = agmod(semicrop[:551]+deband+semicrop[22112:], strength=0.8, size=0.75, static=True, luma_scaling=4)
# grain.set_output(9)

final = depth(grain, 10)
final.set_output(1)
