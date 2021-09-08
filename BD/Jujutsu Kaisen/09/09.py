import vapoursynth as vs
core = vs.core
core.max_cache_size = 8000
core.num_threads = 4

import os
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
from vsutil import plane, join, depth

source = "S01E09-Small Fry and Reverse Retribution.mkv"
source = lvf.src(source)
source = depth(source, 16)

op = r"../JJK v3/00005.m2ts"
op = lvf.src(op)         # this is the OP without credits
op = depth(op, 16)

ed = r"../JJK v1/00006.m2ts"
ed = lvf.src(ed)         # this is the ED without credits
ed = depth(ed, 16)

height = 844

src = source[:6642]+op[:-26]+source[8800:31315]+ed[:-27]+source[33472:]

cred_op = source[6642:8800] # this is the OP with credits
cred_ed = source[31315:33472] # this is the ED with credits


rescale = depth(lvf.scale.descale(clip=src, upscaler=lvf.scale.reupscale(), height=height, kernel=lvf.kernels.Bicubic(b=1/3, c=1/3)), 16)
#dehalo = hvf.DeHalo_alpha(rescale, darkstr=0, brightstr=3)
upscale = join([rescale, plane(src, 1), plane(src, 2)])

    
ref = hvf.SMDegrain(upscale, tr=1, thSAD=84, plane=4)
denoise = mvf.BM3D(upscale, sigma=[2.4, 1.0], ref=ref)

line_mask = kgf.retinex_edgemask(denoise).std.Binarize(9999).rgvs.RemoveGrain(3).std.Inflate()
deband = core.f3kdb.Deband(denoise, range=18, y=64, cb=16, cr=16, grainy=0, grainc=0, output_depth=16, keep_tv_range=True)
deband = core.std.MaskedMerge(deband, upscale, line_mask)


op_fin = atf.ApplyCredits(cred_op, op[:-26], deband[6642:8800])
op_fin = CoolDegrain(op_fin, thsad=16, thsadc=48, blksize=8, overlap=4)

ed_fin = atf.ApplyCredits(cred_ed, ed[:-27], deband[31315:33472])
ed_fin = CoolDegrain(ed_fin, thsad=16, thsadc=48, blksize=8, overlap=4)

mrg = deband[:6642]+op_fin+deband[8800:31315]+ed_fin+deband[33472:]
#den_cred = core.knlm.KNLMeansCL(out, d=2, s=2, h=1.4, device_type='cpu')

grain = agmod(mrg, strength=0.30, size=1, sharp=75, static=True)

final = fvf.Depth(grain, 10)
# final = core.text.Text(final, text="Final")
# final = lvf.diff(source, final)
# source.set_output(0)
final.set_output()
    
# source = core.text.Text(source, text="Source with Creds")
# src = core.text.Text(src, text="Source without Creds")
# source.set_output(0)
# src.set_output(1)
# op.set_output(2)
