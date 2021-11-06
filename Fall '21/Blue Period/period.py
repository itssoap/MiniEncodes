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


key = "[NetflixSucks] Blue Period - 01 (1080p) [F60E48E3].mkv" #key.decode() #"[SubsPlease] Heike Monogatari - 01 (1080p) [516659CC].mkv" #key.decode()
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

line_mask = kgf.retinex_edgemask(upscale).std.Binarize(17000).rgvs.RemoveGrain(3)
line_mask = line_mask.std.Minimum()
# line_mask.set_output(2)

dehalo = core.std.MaskedMerge(src, upscale, line_mask)
dehalo = join([dehalo, plane(src, 1), plane(src, 2)])
# dehalo.set_output(3)

ref = hvf.SMDegrain(dehalo, tr=1, thSAD=64, plane=4)
denoise = mvf.BM3D(dehalo, sigma=[0.4, 0.2], ref=ref)

deband = core.f3kdb.Deband(denoise, range=16, y=64, cb=32, cr=32, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
grain = agmod(deband, strength=0.30, size=0.75, static=True, luma_scaling=6)

# grain.set_output(4)
final = depth(grain, 10)
final.set_output()
