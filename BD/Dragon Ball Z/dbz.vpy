import vapoursynth as vs
core = vs.core

core.max_cache_size = 20000

import os
import edi_rpow2
import havsfunc as hvf
import mvsfunc as mvf
#import fag3kdb
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
import insaneAA
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import plane, join, depth

# reading file and converting to 16bit
key = key.decode()
source = os.path.join(os.getcwd(), key) 

src = lvf.src(source)
#src.set_output()
src = core.std.AssumeFPS(src, fpsnum=24000, fpsden=1001)
src = depth(src, 16)

dehalo = hvf.DeHalo_alpha(src, darkstr=0)
upscale = insaneAA.rescale(dehalo, dx=src.width, dy=src.height)
src = insaneAA.insaneAA(src, external_aa=upscale)
src = join([src, plane(src, 1), plane(src, 2)])

ref = hvf.SMDegrain(src, tr=1, thSAD=100, plane=4)
enc = mvf.BM3D(src, sigma=[5.4, 3.0], ref=ref) # degrain the f*ck outta this raw

line_mask = kgf.retinex_edgemask(enc).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = core.f3kdb.Deband(enc, range=18, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
enc = core.std.MaskedMerge(deband, enc, line_mask)

enc = kgf.adaptive_grain(enc, strength=0.4, luma_scaling=8)
enc = depth(enc, 10)
enc.set_output()
